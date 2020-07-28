from threading import Lock, Thread
from time import sleep

from modules import progress
from modules.networking.http_connect import syn_scan, check
from PyQt5.QtCore import QThread
import socket
import time
import asyncio
import sys
import re


class PortScan(Thread):
    def __init__(self, sig, ports, scan_queue, analyse_queue, mode):
        Thread.__init__(self)
    # def __init__(self, sig, ports, scan_queue, analyse_queue, parent=None):
    #     super(PortScan, self).__init__(parent)
        self.sig = sig
        self.scan_function = syn_scan if mode == 'syn' else check
        self.scan_queue = scan_queue
        self.analyse_queue = analyse_queue
        self.ports = ("9,20-23,25,37,41,42,53,67-70,79-82,88,101,102,107,109-111,"
                 "113,115,117-119,123,135,137-139,143,152,153,156,158,161,162,170,179,"
                 "194,201,209,213,218,220,259,264,311,318,323,383,366,369,371,384,387,"
                 "389,401,411,427,443-445,464,465,500,512,512,513,513-515,517,518,520,"
                 "513,524,525,530,531,532,533,540,542,543,544,546,547,548,550,554,556,"
                 "560,561,563,587,591,593,604,631,636,639,646,647,648,652,654,665,666,"
                 "674,691,692,695,698,699,700,701,702,706,711,712,720,749,750,782,829,"
                 "860,873,901,902,911,981,989,990,991,992,993,995,8080,2222,4444,1234,"
                 "12345,54321,2020,2121,2525,65535,666,1337,31337,8181,6969")\
                  if not ports else ports#list(map(int, ports.split(',')))

        self.isRunning = True
        self.total = progress.get_scan_total()
        # print(self.hosts)
    def run(self):
        while self.isRunning:
            try:
                # print(self.ports)
                with Lock():
                    host = str(self.scan_queue.get())
                    # progress.increment('scan_index')
                asyncio.set_event_loop(asyncio.new_event_loop())
                PortScanner(host, self.ports, self.analyse_queue, self.scan_queue, connection_timeout=5).main()
                # self.ports = ps.parse_ports(self.ports)
                # for port in self.ports:
                #     if self.scan_function(host, port):
                #         # print([host, port])
                #         self.analyse_queue.put(f'{host}:{port}')
                #         progress.increment('discover_total')
            except Exception as e:
                raise e
            finally:
                print(f'\r{round(((262144 - self.scan_queue.qsize())/262144)*100, 2)}', end='')
                state = 0 #if self.total == 0 else (progress.get_scan_index() * 100) / self.total
                # self.sig.send_signal_bar(int(state))
                if state >= 99 and progress.get_actual_action() == 'scanning':
                    progress.increment('action', value='discovering')
                    self.sig.change_actual_action.emit('Discovering')
                    self.stop()



    def stop(self):
        self.isRunning = False


class PortScanner:

    def __init__(self, ip, ports, analyse_queue, scan_queue, connection_timeout=10, queue_size=0):
        self.connection_timeout = connection_timeout
        self.queue_size = queue_size
        self.analyse_queue = analyse_queue
        self.scan_queue = scan_queue
        self.ip = ip
        self.ports = ports

    @staticmethod
    def get_numbers(scan_result):
        scanned_number = 0
        open_number = 0
        for host in scan_result:
            for port, state in scan_result[host]:
                if type(state) is OSError and state.args[0] == 10055:
                    continue
                scanned_number += 1
                if state == 'ok':
                    open_number += 1
        return scanned_number, open_number

    @staticmethod
    def create_queue(input_targets):
        scan_result = dict()
        targets = asyncio.Queue()
        for domain, ports in input_targets.items():
            host = socket.gethostbyname(domain)
            scan_result[host] = []
            for port in ports:
                targets.put_nowait((host, port))
        return targets, scan_result

    async def do_port_tasks(self, port_tasks, scan_result):
        while port_tasks.qsize():
            task = await port_tasks.get()
            ip, port, state = await task
            if type(state) is OSError and state.args[0] == 10055:
                port_tasks.put_nowait(asyncio.create_task(self.check_port(ip, port)))
                return False
            scan_result[ip].append((port, state))
            port_tasks.task_done()
        return True

    async def check_port(self, ip, port):
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.connection_timeout)
            await asyncio.get_event_loop().sock_connect(s, (ip, port))
            print(ip, port, 'ok')
            self.analyse_queue.put(f'{ip}:{port}')
            progress.increment('discover_total')
            return ip, port, 'ok'
        except (PermissionError, ConnectionRefusedError) as e:
            return ip, port, e
        except OSError as e:
            return ip, port, e
        except Exception as e:
            raise e
        finally:
            s.close()

    async def scan_many(self, targets: asyncio.Queue, scan_result):
        port_tasks = asyncio.Queue(self.queue_size)
        is_able = True
        while targets.qsize():
            while is_able and targets.qsize():
                await port_tasks.put(asyncio.create_task(self.check_port(*await targets.get())))
                targets.task_done()
                if port_tasks.full():
                    is_able = await self.do_port_tasks(port_tasks, scan_result)
            while port_tasks.qsize():
                is_able = await self.do_port_tasks(port_tasks, scan_result)
        return scan_result

    def start_scan(self, input_targets: dict):
        targets, scan_result = self.create_queue(input_targets)
        loop = asyncio.get_event_loop()
        scan_result = loop.run_until_complete(self.scan_many(targets, scan_result))
        pending = asyncio.all_tasks(loop)
        asyncio.get_event_loop().run_until_complete(asyncio.gather(*pending))
        return scan_result

    @staticmethod
    def parse_ports(port_string):
        if not re.match(r'[\d\-,\s]+', port_string):
            raise ValueError('Invalid port string')
        ports = []
        port_string = list(filter(None, port_string.split(',')))
        for port in port_string:
            if '-' in port:
                try:
                    port = [int(p) for p in port.split('-')]
                except ValueError:
                    raise ValueError('Negative number')
                for p in range(port[0], port[1] + 1):
                    ports.append(p)
            else:
                ports.append(int(port))
        for port in ports:
            if not (-1 < port < 65536):
                raise ValueError('Ports must be between 0 and 65535')
        return ports

    def main(self):
        ports = self.parse_ports(self.ports)

        start_time = time.time()
        scan_result = self.start_scan({self.ip: ports})
        self.scan_queue.task_done()
# PortScanner().main()