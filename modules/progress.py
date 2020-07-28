from threading import Lock, active_count

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from psutil import cpu_percent, virtual_memory

from modules.paint import green, yellow, red


dead_counter = 0
successful_counter = 0
alive_counter = 0
index = 0
total = 0
scan_index = 0
scan_total = 0
discover_index = 0
discover_total = 0
brute_total = 0
brute_index = 0
isScan = False
result = []
actual_action = str()

def clear():
    global dead_counter, successful_counter, alive_counter, index, total, scan_index, scan_total, discover_index, \
            discover_total, brute_total, brute_index, isScan, result, actual_action
    dead_counter = 0
    successful_counter = 0
    alive_counter = 0
    index = 0
    total = 0
    scan_index = 0
    scan_total = 0
    discover_index = 0
    discover_total = 0
    brute_total = 0
    brute_index = 0
    isScan = True
    result = []
    actual_action = str()

def get_actual_action():
    global actual_action
    with Lock():
        return actual_action

def get_scan_index():
    global scan_index
    with Lock():
        return scan_index

def get_scan_total():
    global scan_total
    with Lock():
        return scan_total

def get_discover_index():
    global discover_index
    with Lock():
        return discover_index


def get_discover_total():
    global discover_total
    with Lock():
        return discover_total


def get_alive_counter():
    global alive_counter
    with Lock():
        return alive_counter


def get_successful_counter():
    global successful_counter
    with Lock():
        return successful_counter


def get_dead_counter():
    global dead_counter
    with Lock():
        return dead_counter


def get_isScan():
    global isScan
    with Lock():
        return isScan

def get_brute_index():
    global brute_index
    with Lock():
        return brute_index

def get_brute_total():
    global brute_total
    with Lock():
        return brute_total

def increment(parameter, value=0):
    global index, alive_counter, successful_counter, dead_counter, \
           isScan, total, brute_index, brute_total, discover_index, discover_total, \
           scan_index, scan_total, actual_action
    with Lock():
        if parameter == 'discover_total':
            discover_total += 1 if value == 0 else value
        elif parameter == 'discover_index':
            discover_index += 1
        elif parameter == 'scan_total':
            scan_total += 1 if value == 0 else value
        elif parameter == 'scan_index':
            scan_index += 1
        elif parameter == 'index':
            index += 1
        elif parameter == 'alive':
            alive_counter += 1
        elif parameter == 'dead':
            dead_counter += 1
        elif parameter == 'successful':
            successful_counter += 1
        elif parameter == 'stop':
            isScan = False
        elif parameter == 'total':
            total = value
        elif parameter == 'brute_index':
            brute_index += 1
        elif parameter == 'brute_total':
            brute_total += 1
        elif parameter == 'action':
            actual_action = value

def update_load_status(sig):
    msg = f'CPU: {colored("cpu")}%<br>Memory: {colored("mem")}%<br>Threads: {active_count()}'
        # print('IT SHOULD WORK')
    sig.change_load_status.emit(msg)

def colored(item):
    load = str(cpu_percent()) if item == 'cpu' else str(dict(virtual_memory()._asdict())["percent"])
    if float(load) < 50:
        return green(load)
    elif float(load) < 80:
        return yellow(load)
    else:
        return red(load)

class Sig(QtCore.QObject):
    change_value = pyqtSignal(str)
    change_progress_str = pyqtSignal(str)
    change_brute_progress_str = pyqtSignal(str)
    change_progressBar = pyqtSignal(int)
    change_dead_counter = pyqtSignal(str)
    change_alive_counter = pyqtSignal(str)
    change_successful_counter = pyqtSignal(str)
    change_actual_action = pyqtSignal(str)
    change_load_status = pyqtSignal(str)
    stop_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(Sig, self).__init__(parent)

    def send_signal(self, value):
        self.change_value.emit(value)

    def send_change_progressBar(self, value):
        global isScan
        if isScan:
            if value == 100:
                isScan = False
            self.change_progressBar.emit(value)
        else:
            self.change_progressBar.emit(100)


