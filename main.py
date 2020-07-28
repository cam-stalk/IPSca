#!/usr/bin/python3
import os
import sys
import re
from random import shuffle
from queue import Queue
from main_ui import *
from netaddr import IPNetwork
from modules.discover import *
from modules.masscan_runner import *
from modules.display import Result
from modules.logger import Logger
from modules.exporter import *
from config import *
from threading import Thread
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QMessageBox, QFileDialog, QVBoxLayout)

from modules.portscan import PortScan


class MyWin(QMainWindow):

    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        QWidget.__init__(self, parent)
        self.ui = Ui_IPSca()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('ipsca.jpg'))

        self.logger = Logger()
        self.Scan = None
        self.IoTOnly = config.IoTOnly
        self.dead_counter = 0
        self.successful_counter = 0
        self.alive_counter = 0
        self.report = {}

        self.ui.scan_btn.clicked.connect(self.click_scan)
        self.ui.import_btn.clicked.connect(self.file_open)
        self.ui.stop_btn.clicked.connect(self.click_stop)
        self.ui.shuffle_btn.clicked.connect(self.shuffle_hosts)
        self.ui.iot_chbx.stateChanged.connect(self.iot_only_change)
        self.ui.brute_chbx.stateChanged.connect(self.brute_enable_change)
        self.ui.submit_export.clicked.connect(self.export)


        self.scan = QThread()



    def export(self):
        format = self.ui.format_combo.currentText()
        #try:
        export = Exporter(format, progress.result)
        export.run()
        self.report = {}
        # while not export.path:
        self.ui.export_path.setText('File(s) was saved: ' + export.path)
        #except Exception as e:
        #print(str(e))
        #pass
        #export.prnt()

    def iot_only_change(self):
        if self.IoTOnly:
            self.IoTOnly = False
        else:
            self.IoTOnly = True

    def brute_enable_change(self):
        if config.brute_enable:
            config.brute_enable = False
        else:
            config.brute_enable = True

    def file_open(self):
        content = []
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)
        if len(name) > 0:
            file = open(name, 'r')
        else:
            return False
        with file:
            try:
                text = file.read().split('\n')
            except:
                QMessageBox.about(self, 'Error', 'Wrong input file')
        for line in text:
            if '	' in line:
                content.append(line.replace('	', ':'))
            elif re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}$", line):
                content.append(line)

        if len(content) == 0:
            QMessageBox.about(self, 'Error', 'Empty input file')
        self.ui.targetsList.setText('\n'.join(content))

    def shuffle_hosts(self):
        hosts = (self.ui.targetsList.toPlainText()).split('\n')
        shuffle(hosts)
        self.ui.targetsList.setText("\n".join(hosts))

    def isRoot(self):
        if os.name == 'nt':
            config.OS = 'windows'
            try:
                os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\\windows'), 'temp']))
            except:
                return False
            else:
                return True
        else:
            if 'SUDO_USER' in os.environ and os.geteuid() == 0:
                return True
            else:
                return False

    def click_scan(self):
        progress.dead_counter = 0
        progress.successful_counter = 0
        progress.alive_counter = 0
        progress.isScan = True

        self.sig = progress.Sig()
        self.sig.change_value.connect(self.update_terminal)
        self.sig.change_progress_str.connect(self.update_progress)
        self.sig.change_brute_progress_str.connect(self.update_brute_progress)
        self.sig.change_progressBar.connect(self.setProgressVal)
        # self.sig.change_progressBar.connect()
        self.sig.change_dead_counter.connect(self.update_dead_label)
        self.sig.change_alive_counter.connect(self.update_alive_label)
        self.sig.change_successful_counter.connect(self.update_successful_label)
        self.sig.change_load_status.connect(self.update_load_status)
        self.sig.change_actual_action.connect(self.update_actual_action)
        self.scan = Scan(self.sig)


        try:
            self.scan.start()
        except Exception as e:
            print(e)

    def click_stop(self):
        progress.isScan = False
        try:
            if True:
                progress.increment('stop')
                for t in self.scan.threads:
                    if t.isRunning:
                        t.stop()
                self.update_terminal(bold("[-] Canceling..."))
                self.sig.send_change_progressBar(100)
                self.scan.isScan = False
                self.ui.action_label.setText('Finish')
        except AttributeError as e:
            print(e)
            pass
        except Exception as e:
            print(e)

    def update_terminal(self, val):
        self.ui.terminal.append(val)

    def clear_terminal(self):
        self.ui.terminal.setText('')

    def update_progress(self, val):
        # sig = self.sig
        self.ui.progress.setText(val)

    def update_brute_progress(self, val):
        # sig = self.sig
        self.ui.progress_2.setText(val)

    def setProgressVal(self, val):
        # print(self.Scan.change_progressBar)
        self.ui.progressBar.setValue(int(val))

    def update_dead_label(self, val):
        self.ui.dead_label.setText(val)

    def update_alive_label(self, val):
        self.ui.alive_label.setText(val)

    def update_successful_label(self, val):
        self.ui.successful_label.setText(val)

    def update_load_status(self, val):
        self.ui.load_status.setText(val)

    def update_actual_action(self, val):
        self.ui.action_label.setText(val)




class Scan(QThread):
    t = []

    def __init__(self, sig, parent=None,):
        super(Scan, self).__init__(parent)
        self.addMassPar = ipsca.ui.addMassParTextbox.text()
        self.HOSTS = (ipsca.ui.targetsList.toPlainText()).split('\n')
        self.SCAN_THREADS = int(ipsca.ui.threads_portscan_edit.text())
        self.sorted_hosts = list()
        self.filter = str(ipsca.ui.filter_line.text())
        self.ports = str(ipsca.ui.portsList.text())
        self.sessions = []
        self.threads = []
        self.single_target = True
        self.logins = default_logins_list
        self.pwds = default_logins_list
        self.sig = sig
        self.scan_queue = Queue()
        self.analyse_queue = Queue()
        self.brute_queue = Queue()
        self.result_queue = Queue()

        progress.increment('total', value=len(self.HOSTS))

        try:
            if len(self.logins) * len(self.pwds) > 200:
                QMessageBox.about(ipsca, 'Error', 'Too many credentials. Max.200')
                progress.isScan = False
            self.THREADS = int(ipsca.ui.threads_edit.text())
            config.timeout = int(ipsca.ui.timeout_edit.text())
        except TypeError:
            QMessageBox.about(ipsca, 'Error', 'Input can only be a number')
            self.isScan = False
        except Exception as e:
            print(e)
            pass

    def update_load(self):
        while progress.isScan:
            progress.update_load_status(self.sig)
            sleep(1)

    @pyqtSlot()
    def run(self):
        # ipsca.ui.terminal.
        self.sig.send_signal(bold('[*] Starting...'))
        for line in self.HOSTS:
            if '/' in line:
                self.single_target = False
                [self.sorted_hosts.append(ip) for ip in IPNetwork(line)]
            else:
                self.sorted_hosts.append(line)
        if self.single_target:
            progress.increment('discover_total', value=len(self.sorted_hosts))
        # shuffle(self.sorted_hosts)
        self.sig.send_signal(bold(f'[*] Loaded {len(self.sorted_hosts)} hosts and {len(self.ports.split(","))} ports.'))
        if not self.single_target:
            ipsca.ui.action_label.setText('Scanning...')
            progress.actual_action = 'scanning'
            progress.increment('scan_total', value=len(self.sorted_hosts))
            if ipsca.isRoot():
                self.sig.send_signal(bold('[!] You are sudo (admin) user. Starting masscan SYN-scan...'))
                scan_worker = Masscan(self.sig, self.ports, self.HOSTS, self.SCAN_THREADS, self.addMassPar, self.analyse_queue)
                scan_worker.setDaemon(True)
                self.threads.append(scan_worker)
                scan_worker.start()
            else:
                [self.scan_queue.put(ip) for ip in self.sorted_hosts]
                mode = 'sock'
                self.sig.send_signal(bold(f'[!] You are {red("NOT")} sudo (admin) user. Starting TCP--scan using sockets...'))

        else:
            progress.increment('action', value='discovering')
            self.sig.change_actual_action.emit('Discovering')
            for i in self.HOSTS:
                self.analyse_queue.put(i)

        # sleep(100)

        display_worker = Result(self.result_queue, self.sig)
        # display_worker.setDaemon(True)
        display_worker.start()

        tt = Thread(target=self.update_load)
        tt.setDaemon(True)
        tt.start()

        if config.brute_enable:
            for _ in range(self.THREADS):
                # analyse_worker = Discover(self.analyse_queue, self.brute_queue, self.sig, self.result_queue)
                analyse_worker = Discover(self)
                # analyse_worker.setDaemon(True)
                self.threads.append(analyse_worker)
                analyse_worker.start()

            for _ in range(self.THREADS):
                brute_worker = Brute(self.brute_queue, self.sig, self.result_queue)
                # brute_worker.setDaemon(True)
                self.threads.append(brute_worker)
                brute_worker.start()
            self.analyse_queue.join()
            self.brute_queue.join()
        else:
            for _ in range(self.THREADS):
                analyse_worker = Discover(self)
                # analyse_worker.setDaemon(True)
                self.threads.append(analyse_worker)
                analyse_worker.start()
            self.analyse_queue.join()
        self.result_queue.join()
        if not progress.isScan:
            ipsca.ui.progressBar.setValue(100)
            self.sig.send_signal(bold('[*] All jobs are finished!'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ipsca = MyWin()
    # Thread(target=ipsca.run).start()
    ipsca.show()
    sys.exit(app.exec_())

