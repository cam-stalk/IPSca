from modules import progress
from modules.networking import http_connect
from modules.paint import green
from urllib.parse import quote as url_encode


def build_url_brute():
    encoded = url_encode(f'cmd=getImageSetting')
    return f'/cgi-bin/CGIProxy.fcgi?{encoded}'


class Foscam:
    def __init__(self, parent):
        print(parent.data)
        self.ip = parent.data['ip']
        self.port = parent.data['port']
        self.auth_type = parent.data['authenticate']
        self.result_queue = parent.result_queue
        self.parent = parent

    def build_url_snap(self, username, password):
        return f'http://{self.ip}/cgi-bin/CGIProxy.fcgi?cmd=snapPicture&usr={username}&pwd={password}'

    def try_for_vuln(self):
        return False

    def connect(self, usr, pwd):
        path = build_url_brute()
        print([self.ip, usr, pwd])
        resp = http_connect.basic_auth_check(self.ip, self.port, usr=usr, pwd=pwd, path=path, returnall=True)
        if resp and '-2' not in resp:
            self.parent.isDone = True
            return True
        return False
