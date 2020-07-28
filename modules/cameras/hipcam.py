from modules import progress
from modules.networking import http_connect
from modules.paint import green


class HipCam:
    def __init__(self, parent):
        self.ip = parent.data['ip']
        self.port = parent.data['port']
        self.result_queue = parent.result_queue
        self.parent = parent

    def try_for_vuln(self):
        if self.connect('user', 'user'):
            return True
        return False

    def connect(self, usr, pwd):
        if http_connect.basic_auth_check(self.ip, self.port, usr=usr, pwd=pwd):
            self.parent.data['usr'] = usr
            self.parent.data['pwd'] = pwd
            self.result_queue.put(self.parent.data)
            progress.increment('successful')
            self.parent.sig.change_successful_counter.emit(green(str(progress.get_successful_counter())))
            self.parent.isDone = True
            return True
        else:
            return False
