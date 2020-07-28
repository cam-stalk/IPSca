from threading import Lock
import psutil
import requests
import urllib3

from requests import get, Session

from modules.analyser import Analyser
from modules.bruteforce import *
from PyQt5.QtCore import QThread



class Discover(QThread):

    def __init__(self, parent):
        QThread.__init__(self)
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US)'}
        self.parent = parent
        self.analyse_queue = self.parent.analyse_queue
        self.brute_queue = self.parent.brute_queue
        self.result_queue = self.parent.result_queue
        self.sig = self.parent.sig
        self.repeat_counter = 0
        self.previous = dict()
        self.analyse = Analyser
        self.isRunning = True
        self.bruteOnly = False
        self.iot_only = config.IoTOnly
        self.bruteEnable = config.brute_enable
        self.total = progress.get_discover_total()
        # self.sig.change_progress_str.connect()
        self.filter = ''#str(ipsca.ui.filter_line.text())
        self.host = None
        self.TIMEOUT = config.timeout
        self.headers = {}
        self.result = dict()

    def set_default(self):
        self.host = None
        self.result = dict()
        self.result = {'host': ':',
                       'ip': None,
                       'port': None,
                       'usr': None,
                       'pwd': None,
                       'ch': 1,
                       'vendor': None,
                       'device': None,
                       'vuln': False,
                       'authmethod': None,
                       'authservice': None,
                       'authenticate': None,
                       'realm': None,
                       'resp': None,
                       'msg': None}
    def stop(self):
        print('DISCOVER - STOP!!!')
        self.isRunning = False

    def run(self):
        # self.sig.stop_signal.connect(lambda: self.stop())
        while self.isRunning:
            self.set_default()
            with Lock():
                self.host = self.analyse_queue.get()
            # print(self.host)
            self.result.update({'host': self.host,
                                'ip': self.host.split(':')[0],
                                'port': self.host.split(':')[1]})
            self.worker()
            self.analyse_queue.task_done()
        return

    def worker(self):
        try:
            progress.increment('discover_index')
            index = progress.get_discover_index()
            self.total = progress.get_discover_total()
            dead_counter = progress.get_dead_counter()

            self.sig.change_progress_str.emit(bold(f'[{index}/{progress.get_discover_total()}] {self.host}'))
            response = get(f'http://{self.host}', timeout=self.TIMEOUT, headers=self.headers)
            self.result.update({'host': response.url.split('/')[2]})
            progress.increment('alive')
            self.sig.change_alive_counter.emit(str(index - dead_counter))

            if self.filter not in str(response.headers):
                return False
            self.analyse = Analyser(response.headers, response.text)
            if self.analyse.done:
                # vuln = ''
                result, device, vendor, authmethod, authservice, authenticate, = self.analyse.make_results()
                self.result.update({  'vendor': vendor,
                                      'device': device,
                                      'vuln': True if 'VULN' in result else False,
                                      'authmethod': authmethod,
                                      'authservice': authservice,
                                      'authenticate': authenticate,
                                      'realm': '',
                                      'resp': response})

                if self.bruteEnable:
                    self.brute_queue.put(self.result)
                    progress.increment('brute_total')
                else:
                    self.result_queue.put(self.result)
                return
            # 190.160.70.84:1024
            if self.iot_only:
                return False
            if 'WWW-Authenticate' in str(response.headers):
                #print(response.headers['WWW-Authenticate'])
                self.result['authenticate'] = str(response.headers['WWW-Authenticate'])
                self.result['ip'], self.result['port'] = self.result['host'].split(':')
                self.result['resp'] = response
                if self.bruteEnable:
                    self.brute_queue.put(self.result)
                    progress.increment('brute_total')
                return
                # self.send_signal(gray(f"[{gray(bold(host))}][{(response.headers['WWW-Authenticate']).split(',')[0]}] {result}"))
            if 'Server' in str(response.headers) and not self.iot_only:
                # self.send_signal(f"[{gray(bold(host))}] {yellow(prepare_html(response))}")
                self.result['msg'] = response.headers['Server']
                self.result['resp'] = response
            elif not self.iot_only:
                self.result['msg'] = "WEB"
                self.result['resp'] = response
            else:
                return
            with Lock():
                self.result_queue.put(self.result)
                # print(prepare_html(response))


            # if ipsca.brute_enable:

            #         if vendor == 'Hikvision':
            #             #brute = Brute_Hik(ipsca.report[host]['ip'], ipsca.report[host]['authenticate'])дщ
            #             brute = Brute_Hik(ipsca.report[self.host]['url'], ipsca.report[self.host]['authservice'])
            #             # print(ipsca.report[host])
            #             if brute.vuln:
            #                 progress.send_signal(f"[{gray(bold(host))}]{result}{red(bold('VULN'))}")
            #                 ipsca.report[host].update({'VULN': True})
            #                 return
            #         elif vendor == 'Foscam':
            #             brute = Brute_Foscam(ipsca.report[host]['url'])
            #         elif vendor == 'Netwave':
            #             response = requests.get(f'{ipsca.report[host]["url"]}get_camera_params.cgi', timeout=self.TIMEOUT, headers=self.headers)
            #             ipsca.report[host].update({'url': response.url})
            #             brute = Brute_GET(ipsca.report[host])
            #         elif vendor == 'Dahua':
            #             response = requests.get(f'http://{ipsca.report[host]["url"]}'
            #                                     f'/current_config/passwd',
            #                                     timeout=self.TIMEOUT, headers=self.headers)
            #             response2 = requests.get(f'http://{ipsca.report[host]["url"]}'
            #                                     f'/current_config/Account1',
            #                                     timeout=self.TIMEOUT, headers=self.headers)
            #             if response.status_code == 200 or response2.status_code == 200:
            #                 ipsca.report[host].update({'VULN': True})
            #                 brute = False
            #                 creds = ''
            #             else:
            #                 #ipsca.report[host].update({'url': response.url})
            #                 #brute = Brute_GET(ipsca.report[host], self.logins, self.pwds)
            #                 pass
            #         else:
            #             brute = Brute_GET(ipsca.report[host], self.logins, self.pwds)
            #         if brute:
            #             brute.start()
            #             creds = brute.make_results()
            #         if len(creds) > 0 and ':' in creds:
            #             usr, pwd = creds.split(':')
            #             ipsca.successful_counter += 1
            #             ipsca.report[host].update({'usr': usr, 'pwd': pwd})
            #             if ipsca.report[host]['authservice'] == 'DNVRS-Webs':
            #                 ipsca.report[host].update({'numb_of_ch': brute.get_channels_number()})
            #             creds = f'[{creds}]'
            #     else:
            #         creds = ''
            #     if ipsca.report[host]['VULN']:
            #         vuln = '[VULN]'
            #     self.send_signal(f"[{gray(bold(host))}]{result}{red(bold(vuln))}{red(creds)}")
            # elif 'WWW-Authenticate' in str(response.headers) and not ipsca.IoTOnly:
            #     #print(response.headers['WWW-Authenticate'])
            #     ipsca.report[host] = {'ip': host, 'authenticate': str(response.headers['WWW-Authenticate'])}
            #     if ipsca.brute_enable:
            #         brute = Brute_GET(ipsca.report[host])
            #         brute.start()
            #         result = f'[{brute.make_results()}]'
            #     else:
            #         result = ''
            #     self.send_signal(gray(f"[{gray(bold(host))}][{(response.headers['WWW-Authenticate']).split(',')[0]}] {result}"))
            # elif 'Server' in str(response.headers) and not ipsca.IoTOnly:
            #     self.send_signal(f"[{gray(bold(host))}] {yellow(prepare_html(response))}")
            #     # print(prepare_html(response))
            # elif not ipsca.IoTOnly:
            #     self.send_signal(f"[{gray(bold(host))}] {yellow(prepare_html(response))}")
            #     # print(prepare_html(response))
        except ConnectionError as e:
            # print(e)
            progress.increment('dead')
            return
        except requests.exceptions.ReadTimeout:
            progress.increment('dead')
            return
        except urllib3.exceptions.ReadTimeoutError:
            progress.increment('dead')
            return
        except Exception as e:
            progress.increment('dead')
            # self.sig.send_signal(red(self.host + ' - ' + str(e)))
            # self.result_queue.put({'host': self.host, 'msg': red(str(e))})
            if 'BadStatusLine' in str(e):
                self.result['msg'] = red('NOT http: ') + str(e).split("'")[3]
                with Lock():
                    self.result_queue.put(self.result)
            return
        finally:
            # if config.brute_enable and progress.get_brute_total() > 0:
            #     state = int((progress.get_index() * 100) / self.total)
            #             # (progress.get_brute_index()*100) / progress.get_brute_total()/2
            # else:
            if progress.actual_action == 'discovering':
                state = 0 if self.total == 0 else (progress.get_discover_index() * 100) / self.total
                self.sig.send_change_progressBar(int(state))
                self.sig.change_dead_counter.emit(red(str(progress.get_dead_counter())))
                if state >= 99 and progress.actual_action == 'discovering':
                    if self.bruteEnable:
                        progress.increment('action', value='bruteforcing')
                        self.sig.change_actual_action.emit('Bruteforcing...')
                        self.stop()
                    else:
                        self.sig.change_actual_action.emit('DONE')
                        self.stop()
                    self.stop()
            # self.update_load_status()




