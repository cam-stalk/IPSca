import re
from threading import Lock, Thread

import config
from modules import progress
import sys
from tempfile import TemporaryFile
from time import sleep
from subprocess import Popen, STDOUT


class Masscan(Thread):
    def __init__(self, sig, ports, targets, rate, addMassPar, analyse_queue):
        Thread.__init__(self)
        self._write_tmp_hosts(targets)
        self.sig = sig
        self.analyse_queue = analyse_queue
        self.rate = rate
        self.ports = ("9,20-23,25,37,41,42,53,67-70,79-82,88,101,102,107,109-111,"
                 "113,115,117-119,123,135,137-139,143,152,153,156,158,161,162,170,179,"
                 "194,201,209,213,218,220,259,264,311,318,323,383,366,369,371,384,387,"
                 "389,401,411,427,443-445,464,465,500,512,512,513,513-515,517,518,520,"
                 "513,524,525,530,531,532,533,540,542,543,544,546,547,548,550,554,556,"
                 "560,561,563,587,591,593,604,631,636,639,646,647,648,652,654,665,666,"
                 "674,691,692,695,698,699,700,701,702,706,711,712,720,749,750,782,829,"
                 "860,873,901,902,911,981,989,990,991,992,993,995,8080,2222,4444,1234,"
                 "12345,54321,2020,2121,2525,65535,666,1337,31337,8181,6969") if not ports else ports
        self.parameters = []
        self.parameters = list()
        self.parameters.append('--randomize-hosts')
        self.parameters.append('--http-user-agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"')
        self.parameters.append('-p' + self.ports)
        self.parameters.append('-iL tmp')
        # self.parameters.append('-p ' + self.ports)
        self.parameters.append('--rate ' + str(self.rate))
        self.parameters.append(addMassPar)
        self.sub = None

        # rate:  0.00-kpps, 100.00% done, waiting 5-secs, found=9
        self.isRunning = True
        self.total = progress.get_scan_total()
        # print(self.hosts)
    def run(self):
        while self.isRunning:
            tmp = TemporaryFile()
            try:
                masscan = 'masscan' if config.OS == 'windows' else 'sudo masscan'
                self.sub = Popen(f'{masscan} {" ".join(self.parameters)}', stdout=tmp, stderr=STDOUT, shell=True)
                while self.sub.poll() is None:
                    where = tmp.tell()
                    lines = tmp.read()
                    if not lines:
                        sleep(0.01)
                        tmp.seek(where)
                    else:
                        lines = lines.decode().split('\n')
                        for line in lines:
                            if line.startswith('Discovered'):
                                self.analyse_queue.put(self._line_processing(line))
                                progress.increment('discover_total')
                            elif line.startswith('rate'):
                                state = re.findall(r'\d{1,2}.\d{1,2}%', line)
                                state = ''.join(state).replace('%', '')
                                self.sig.send_change_progressBar(int(float(state)))
                                self.sig.change_actual_action.emit(line)
                sys.__stdout__.write((tmp.read()).decode())
                sys.__stdout__.flush()
            except Exception as e:
                print(f'{__name__} - {e}')
            finally:
                self.sub.kill()
                progress.increment('action', value='discovering')
                self.sig.change_actual_action.emit('Discovering...')
                break

    def _line_processing(self, line):
        return line.split(' ')[5] + ':' + line.split(' ')[3].replace('/tcp', '')

    def _write_tmp_hosts(self, hosts):
        with open('tmp', 'w') as f:
            f.write("\n".join(hosts))
        return



    def stop(self):
        self.sub.kill()
        self.isRunning = False