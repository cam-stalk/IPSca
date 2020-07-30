import base64
import socket

from idna import unicode
from requests.auth import HTTPDigestAuth
from requests import get
import config
from scapy.all import *


def basic_auth_check(ip, port, usr=None, pwd='', returnall=False, path='/', cookie=None, decode=True):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as con:
            path = path.encode()
            con.connect((ip, int(port)))
            con.settimeout(config.timeout)
            packet =  b"GET %s HTTP/1.1\r\n" % path
            packet += b"Host: %s\r\n" % (ip + ':' + port).encode()
            packet += b"Connection: close\r\n"
            if usr:
                token = base64.b64encode(b'%s:%s' % (usr.encode(), pwd.encode()))
                packet += b"Authorization: Basic %s\r\n" % token
            if cookie:
                packet += b"Cookie: %s\r\n" % cookie.encode()
            packet += b"\r\n"
            con.send(packet)
            # return con.recv(1024).decode()
            if returnall:
                if decode:
                    return con.recv(1024).decode('utf-8', 'replace')
                else:
                    print('!!!!!!!!!!!!!!!!!!!')
                    data = con.recv(1024).decode()
                    return data
            else:
                data = (con.recv(12)).decode('utf-8', 'replace').split(' ')
        # print(data)
        if len(data) < 2:
            return False
        if data[1] == '401':
            return False
        elif data[1] == '404':
            return False
        elif data[1] == '200':
            return True
        return False
    except socket.timeout:
        pass
    except Exception as e:
        print(f'{__name__} - {ip} - {e}')
        return False

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data.decode()

def check(ip, port_number):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(1)
    try:
        sock.connect((ip, port_number))
        return True
    except Exception as e:
        # print(e)
        return False

def syn_scan(target, port):
    # print("syn scan on, %s with ports %s" % (target, port))
    sport = RandShort()
    pkt = sr1(IP(dst=target)/TCP(sport=sport, dport=port, flags="S"), timeout=1, verbose=0)
    if pkt != None:
        if pkt.haslayer(TCP):
            if pkt[TCP].flags == 20:
                return False
                # print(str(port) + " - " + "Closed")
            elif pkt[TCP].flags == 18:
                # print(str(port) + " - " + "Open")
                return True

def digest_auth_check(ip, port, usr='', pwd='', path='', returnall=False):
    auth = HTTPDigestAuth(usr, pwd)
    try:
        r = get(f'http://{ip}:{port}{path}', auth=auth)
    except:
        return False
    if returnall:
        return r
    elif str(r) == '<Response [200]>' and 'Object Not Found' not in r.text:
        # print(r.text)
        return True
    else:
        return False

# if 'Basic' in auth_type else \
#                 hashlib.md5(b'%s:%s' % (usr.encode(), pwd.encode())).hexdigest()