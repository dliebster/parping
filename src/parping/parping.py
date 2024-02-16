#!/usr/bin/python
#
# pyping.py, a parallel ip pinging utility.
#
# Dan Liebster. Mostly plagiarized, no idea how any of this stuff works. Things could have been cleaner, tried to stick with stock libs.
# Currently supported on Linux, macOS, and Windows.Aix SHOULD have worked with the default ping arguements, but as anticipated...
# IP input is a list of ip addresses to ping
#
#

import os
import sys
import subprocess
import platform
import re
import socket
import ipaddress

ostype = platform.system()
FNULL = open(os.devnull, 'w')
indata = "none"
ips = []
iplist = []


def valid_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        return False


class Parping():
    def __init__(self):
        self.address = None
        self.ostype = platform.system()
        self.FNULL = open(os.devnull, 'w')
        self.indata = "none"
        self.ips = []
        self.iplist = []
        # The following is regex to check if an ip address was supplied as an arg.
        # Being supplanted by socket.si
        # self.ippatt = re.compile(
        #    ('^([2][0-5][0-5]|^[1]{0,1}[0-9]{1,2})'
        #     '\.([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})'
        #     '\.([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})'
        #     '\.([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})$'
        #     ))

    @classmethod
    def parping_range(self, ip_addr, ip_mask):
        # ips_in = array of ip addresses
        # TODO move OS detection up one level
        goodip = badip = 0
        ip_cidr = f'{ip_addr}/{ip_mask}'

        p = {}

        print(f'parsing {ip_cidr}')
        for ip in ipaddress.IPv4Network(ip_cidr, strict=False):
            ip = str(ip)
            print(f'prepinging {ip}')

            if ostype == "Darwin":
                print("Darwin/MacOS detected..")
                print(f'Adding {ip} to iplist..')
                p[ip] = subprocess.Popen(['ping', '-n', '-W2', '-c2', ip], stdout=FNULL, stderr=subprocess.STDOUT)
            elif ostype == "Windows":
                print("Windows OS detected..")
                p[ip] = subprocess.Popen(['ping', '-w', '1000', '-n', '2', ip], stdout=FNULL, stderr=subprocess.STDOUT)
            else:
                print("Linux detected..")
                p[ip] = subprocess.Popen(['ping', '-n', '-w2', '-c2', ip], stdout=FNULL, stderr=subprocess.STDOUT)

        while p:
            for ip, proc in p.items():
                if proc.poll() is not None:
                    del p[ip]
                    retcode = proc.returncode
                    if proc.returncode == 0:
                        print('{0} active'.format(ip))
                        goodip += 1
                    elif proc.returncode == 1:
                        print('{0} no response'.format(ip))
                        badip += 1
                    else:
                        # refactoring print('{0} returned error {1}'.format(ip))
                        print('{0} returned error'.format(ip))
                        badip += 1
                    break

        print('\nSummary:\n{} responding IPs.'.format(goodip))
        print('{} non-responding IPs'.format(badip))

        return goodip, badip
