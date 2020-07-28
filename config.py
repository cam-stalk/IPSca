from threading import Lock

from modules.tools import *

default_logins_list = read_file('dict/logins.txt')
default_passwords_list = read_file('dict/passwords.txt')
hik_logins_list = read_file('dict/logins_hik.txt')
hik__passwords_list = read_file('dict/passwords_hik.txt')
brute_enable = False
IoTOnly = False
OS = 'nix'
timeout = 1


def get_brute_enable():
    global brute_enable
    with Lock():
        return brute_enable

# def set_logins(file):
#     global logins_list
#     logins_list = read_file(file)
#
# def set_passwords(file):
#     global passwords_list
#     passwords_list = read_file(file)
