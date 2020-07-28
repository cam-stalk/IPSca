import threading
from time import sleep

import requests
from PyQt5.QtCore import QThread

from modules import progress
from modules.paint import *
from modules.tools import prepare_html


class Result(QThread):

    def __init__(self, result_queue, sig):
        super(Result, self).__init__()
        self.result_queue = result_queue
        self.sig = sig
        self.previous = ''
        self.total = progress.get_discover_total()

    def build_terminal_line(self, data):
        vuln = 'Vulnerability'
        if data['device']:
            if data['vuln']:
                return bold(f'[{yellow(data["host"])}][{blue(data["device"])}][{green(data["vendor"])}][{red(vuln)}]')
            elif data['usr']:
                return bold(f'[{yellow(data["host"])}][{blue(data["device"])}][{green(data["vendor"])}][{red(data["usr"] + ":" + data["pwd"])}]')
            else:
                return bold(f'[{yellow(data["host"])}][{blue(data["device"])}][{green(data["vendor"])}]')
        else:
            if data['usr']:
                return bold(f'[{yellow(data["host"])}][{blue(data["resp"].headers["WWW-Authenticate"])}][{red(data["usr"] + ":" + data["pwd"])}]')
            if str(data['resp']) == '<Response [401]>' and not data['msg']:
                line = f'[{yellow(data["host"])}]'
                if "Server" in data["resp"].headers:
                    line += f'[{blue(data["resp"].headers["Server"])}]'
                else:
                    f'[{yellow(data["host"])}]'
                if data['authenticate']: return line + f'[{data["authenticate"]}]'
            elif data['msg']:
                if type(data['resp']) == requests.models.Response:
                    return f'[{yellow(data["host"])}][{blue(data["msg"])}][{prepare_html(data["resp"])}]'
                else:
                    return f'[{yellow(data["host"])}][{blue(data["authenticate"])}]'
            else:
                return bold(f'[{yellow(data["host"])}]')

    def run(self):
        while True:
            with threading.Lock():
                data = self.result_queue.get()
                if not data == self.previous:
                    progress.result.append(data)
                    # print(data)
                    result = self.build_terminal_line(data)
                    if result:
                        self.sig.send_signal(result)
                self.previous = data
            self.result_queue.task_done()
            sleep(0.01)

