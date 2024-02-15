#!/usr/bin/python
#
# pyping.py, a parallel ip pinging utility.
#
# Dan Liebster. Mostly plagiarized, no idea how any of this stuff works. Things could have been cleaner, tried to stick with stock libs.
# Currently supported on Linux, MacOS, and Windows.Aix SHOULD have worked with the default ping arguements, but as anticipated...
# IP input is either iprange of class Cs, e.g 10.100.11.1-50, or defaults to looking for a local file named "iplist" expecting an IP per line..
#
# Usage examples:  ./pyping.py 10.100.11.1-120     ||     ./pyping.py (will look in local dir for file named iplist)
#
# Current version: 0.4 @ 12-13-2016.


import os
import sys
import subprocess
import platform
import re

ostype = platform.system()
FNULL = open(os.devnull, 'w')
indata = "none"
ips = []
iplist = []
# The following is regex to check if an ip address was supplied as an arg.
ippatt = re.compile(
    ('^([2][0-5][0-5]|^[1]{0,1}[0-9]{1,2})'
     '\.([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})'
     '\.([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})'
     '\.([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})$'))

while indata == "none":
    if len(sys.argv) > 1:

        indata = "cli"
        userargs = sys.argv[1]
        ipmatch = re.search(ippatt, userargs.split("-")[0])

        if ipmatch:

            iprange = userargs.split(".")
            a = iprange[0]
            b = iprange[1]
            c = iprange[2]
            d = iprange[3]

            drange = d.split("-")
            dbegin = int(drange[0])
            dend = int(drange[1])

            index = dbegin

            while index <= dend:
                itemip = a + "." + b + "." + c + "." + str(index)
                ips.append(itemip)
                index += 1


    else:
        indata = "filelist"
        try:
            ipfile = open('iplist', 'r')
        except IOError as e:
            print(
                "\n\n Expecting to find file named \"iplist\" given the lack of subnet iprange argument. ({0}): {1}\n\n".format(
                    e.errno, e.strerror))
            exit()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        for item in ipfile:
            ips.append(item)


def parping_all(ips_in):
    goodip = badip = 0

    p = {}
    for ip in ips_in:
        if not ip.isspace():
            if ostype == "Darwin":
                p[ip] = subprocess.Popen(['ping', '-n', '-W2', '-c2', ip], stdout=FNULL, stderr=subprocess.STDOUT)
            elif ostype == "Windows":
                p[ip] = subprocess.Popen(['ping', '-w', '1000', '-n', '2', ip], stdout=FNULL, stderr=subprocess.STDOUT)
            else:
                p[ip] = subprocess.Popen(['ping', '-n', '-w2', '-c2', ip], stdout=FNULL, stderr=subprocess.STDOUT)

    while p:
        for ip, proc in p.items():
            if proc.poll() is not None:
                del p[ip]
                retcode = proc.returncode
                if proc.returncode == 0:
                    print('{0} active'.format(ip.rstrip()))
                    goodip += 1
                elif proc.returncode == 1:
                    print('{0} no response'.format(ip.rstrip()))
                    badip += 1
                else:
                    print('{0} returned error {1}'.format(ip.rstrip(), retcode))
                    badip += 1
                break

    print('\nSummary:\n{} IPs responded.'.format(goodip))
    print('{} did not.'.format(badip))

    return goodip, badip
