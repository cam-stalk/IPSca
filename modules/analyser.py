from modules.paint import *
from modules.tools import cut
from functools import lru_cache


# logger = Logger()

class Analyser:

    def __init__(self, headers, content):

        self.headers = headers
        self.headers.update({"title": cut(content, '<title>', '</title>')})
        self.data = {'headers': self.headers}
        self.device = ''
        self.vendor = ''
        self.authservice = ''
        self.authmethod = 'WWW-Authenticate' if 'WWW-Authenticate' in self.data['headers'] \
            else 'Server' if 'Server' in self.data['headers'] else ''
        self.authenticate = '' if 'WWW-Authenticate' not in self.data['headers'] else self.data['headers']['WWW-Authenticate']
        self.vulnerabilities = ['uc-httpd 1.0.0',  'P3P: CP=CAO PSA OUR', 'GoAhead+5ccc069c403ebaf9f0171e9517f40e41&'] #'thttpd/2.25b',
        self.devices ={'IPCAM': {'Hipcam': ['Basic realm="index.html"'],
                                    'Dahua': ['WEB SERVICE', 'CP=CAO PSA OUR'],
                                    'Hikvision': ['App-webs/', 'DNVRS-Webs', 'DVRDVS-Webs', 'Hikvision-Webs', 'webserver', 'DVS-Webs'],
                                    'GoAhead': ['Digest realm="WIFICAM"', 'Basic realm="Internet Camera"',
                                                'GoAhead-http', 'Digest realm="goAhead"', 'Digest realm="GoAhead"',
                                                'Basic realm="GoAhead"',  'realm="Vstarcam"',
                                                'realm="IPCAM"', 'realm="iPNOVA"', 'realm="iCAM"', 'realm="camera"',
                                                'realm="BlueCAM"'],
                                    'ActiveCam': ['ActiveCam'],
                                    'DBELL': ['dbell'],
                                    # 'NETSurveillance': ['uc-httpd 1.0.0'],
                                    'BEWARD': ['N100 H.264 IP Camera'],
                                    'D-Link': ['DCS-', 'DI-', 'dcs-lig-httpd'],
                                    'AXIS': ['AXIS'],
                                    'Foscam': ['IPCam Client', 'uc-httpd 1.0.0', 'thttpd/2.25b 29dec2003'],
                                    'Netwave': ['Netwave IP Camera'],
                                    'iCatch': ['mini_httpd', 'Basic realm=""', 'Basic realm="DVR"', 'Basic realm="."'],
                                    'Brickcom': ['realm="OB-', 'realm="WOB-', 'realm="Brickcom'],
                                    'Linksys': ['realm="Linksys'],
                                    'Tenvis': ['realm="IPCamera"'],
                                    'Undefined': ['WebCam', 'Camera', 'DVR', 'NVR']},
                        # 85.93.147.157:8010
                        'ROUTER': {'TP-LINK': ['TP-LINK', 'TL-WR'],
                                    'ZyXEL': ['ZyXEL', 'KEENETIC GIGA'],
                                    'D-LINK': ['D-LINK', 'DIR-'],
                                    'ASUS': ['RT-N', 'RT-G', 'RT-AC', 'RT-AX', 'RT-AC87U'],
                                    'CISCO': ['level_15 or view_access', 'level_15_access'],
                                    'DD-WRT': ['DD-WRT'],
                                    'Huawei': ['HuaweiHomeGateway'],
                                    'U.S. Robotics': ['realm="U.S. Robotics'],
                                    'MikroTik': ['Mikrotik'],
                                    'SMC': ['GoAhead-Webs SMC'],
                                    'Intelbras': ['realm="WIN', 'RF 301K'],
                                    'DrayTek': ['VigorFly210'],
                                    'Buffalo': ['realm="AirStation'],
                                    'NETGEAR': ['realm="NETGEAR']},
                        'SERVER': {'SUPERMICRO': ['2423']}}

        self.done = self.identifying_device()
        self.vulnerability = self.isVulnerability()

    @lru_cache(maxsize=32)
    def identifying_device(self):
        if len(self.authservice) == 0 and len(self.authmethod) > 0:
            for dev in self.devices:
                for vend in self.devices[dev]:
                    if any([sign in self.data['headers'][self.authmethod] for sign in self.devices[dev][vend]]):
                        for sign in self.devices[dev][vend]:
                            if sign in self.data['headers'][self.authmethod]:
                                self.authservice = sign
                        self.device = dev
                        self.vendor = vend
                        return True
        elif len(self.data['headers']['title']) > 0:
            for dev in self.devices:
                for vend in self.devices[dev]:
                    if any([sign in self.data['headers']['title'] for sign in self.devices[dev][vend]]):
                        for sign in self.devices[dev][vend]:
                            if sign in self.data['headers']['title']:  # or sign in self.data['title']:
                                self.authservice = sign
                        self.device = dev
                        self.vendor = vend
                        return True
        elif len(self.data['headers']['Content-Length']) > 0:
            for dev in self.devices:
                for vend in self.devices[dev]:
                    if any([sign == self.data['headers']['Content-Length'] for sign in self.devices[dev][vend]]):
                        self.device = dev
                        self.vendor = vend
                        return True
        return False

    def isVulnerability(self):
        for vul in self.vulnerabilities:
            if vul in self.data:
                return True
        return False

    @lru_cache(maxsize=2)
    def make_results(self):
        res = f'[{green(self.vendor)}][{blue(self.device)}]'
        if self.vulnerability:
            res += f'[{red("VULN")}]'
        return bold(res), self.device, self.vendor, self.authmethod, self.authservice, self.authenticate
