from modules.paint import *


def read_file(file):
    with open(file, 'r') as f:
        return f.read().split('\n')


def cut(content, begin, end):
    idx1 = content.find(begin)
    idx2 = content.find(end, idx1)
    return content[idx1+len(begin):idx2].strip()


def build_terminal_line(host, vendor='unknown', vuln=False, usr=False, pwd='', msg=None, resp=None):
    if vuln:
        return bold(f'[{yellow(host)}][{green(vendor)}][{red("VULN")}]')
    elif usr:
        return bold(f'[{yellow(host)}][{green(vendor)}][{red(usr+":"+pwd)}]')
    elif resp:
        return bold(f'[{yellow(host)}][{yellow(prepare_html(resp))}]')
    elif msg:
        return bold(f'[{yellow(host)}][{green(vendor)}][{yellow(msg)}]')
    else:
        return bold(f'[{yellow(host)}][{green(vendor)}]')


def prepare_html(response):
    try:
        server = response.headers['Server']
    except KeyError:
        server = 'Unknown'
    title = cut(response.text, '<title>', '</title>') \
        if 'JavaScript' not in cut(response.text, '<title>', '</title>') and 'title' in response.text \
        and 'Connect failed' not in cut(response.text, '<title>', '</title>') \
        and 'No server or forwarder data' not in cut(response.text, '<title>', '</title>') else ''
    h1 = cut(response.text, '<h1>', '</h1>') \
        if 'JavaScript' not in cut(response.text, '<title>', '</title>') and 'h1' in response.text \
        and 'No server or forwarder data' not in cut(response.text, '<title>', '</title>') \
        and 'Connect failed' not in cut(response.text, '<title>', '</title>') else ''
    return (f'{server} {title}\n{h1}')[:150]