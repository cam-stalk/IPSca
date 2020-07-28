from modules import progress
from modules.networking import http_connect
from modules.paint import green


class GoAhead:
    def __init__(self, parent):
        self.ip = parent.data['ip']
        self.port = parent.data['port']
        self.result_queue = parent.result_queue
        self.parent = parent

    def try_for_vuln(self):
        if 'Basic' in self.parent.data['authenticate']:
            if http_connect.basic_auth_check(self.ip, self.port, 'admin', 'admin'):
                self.set_done('admin', 'admin')
                return True
        elif 'Digest' in self.parent.data['authenticate']:
            if http_connect.digest_auth_check(self.ip, self.port, 'admin', 'admin'):
                self.set_done('admin', 'admin')
                return True

        r = False#http_connect.basic_auth_check(self.ip, self.port, path="/cgi-bin/c8fed00eb2e87f1cee8e90ebbe870c190ac3848c", returnall=True)
        if not r:
            return False
        if r.find("CGI process file does not exist") != -1:
            self.parent.data['vuln'] = "CGI scripting is enabled"
            return True
        else:
            return False

    def connect(self, usr, pwd):
        if 'Basic' in self.parent.data['authenticate']:
            if http_connect.basic_auth_check(self.ip, self.port, usr=usr, pwd=pwd):
                self.set_done(usr, pwd)
                return True
        elif 'Digest' in self.parent.data['authenticate']:
            resp = http_connect.digest_auth_check(self.ip, self.port, usr=usr, pwd=pwd, returnall=True)
            if str(resp) == '<Response [200]>':
                if len(resp.text) > 256:
                    self.set_done(usr, pwd)
                    return True
        return False

    def set_done(self, usr, pwd):
        self.parent.data['usr'] = usr
        self.parent.data['pwd'] = pwd
        self.result_queue.put(self.parent.data)
        progress.increment('successful')
        self.parent.sig.change_successful_counter.emit(green(str(progress.get_successful_counter())))
        self.parent.isDone = True