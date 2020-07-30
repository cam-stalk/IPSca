from modules import progress
from modules.networking import http_connect
from modules.paint import green
from urllib.parse import quote as url_encode



class Dlink:
    def __init__(self, parent):
        self.ip = parent.data['ip']
        self.port = parent.data['port']
        self.auth_type = parent.data['authenticate']
        self.path = '/eng/index.html'
        self.cookie = 'language=eng'
        self.result_queue = parent.result_queue
        self.parent = parent

    def build_url_snap(self, username, password):
        return f'http://{self.ip}/cgi-bin/CGIProxy.fcgi?cmd=snapPicture&usr={username}&pwd={password}'

    def try_for_vuln(self):
        return False

    def connect(self, usr, pwd):
        path = self.path
        if http_connect.basic_auth_check(self.ip, self.port, usr=usr, pwd=pwd, path=path, cookie=self.cookie):
            self.parent.data['usr'] = usr
            self.parent.data['pwd'] = pwd
            self.parent.isDone = True
            return True
        return False
