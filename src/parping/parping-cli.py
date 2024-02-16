#!/usr/bin/env python3
#
# pyping.py, a parallel ip pinging utility.
#
# Dan Liebster
#
# Currently supported on Linux, MacOS, and Windows. AIX SHOULD have worked with the default ping arguements, but as anticipated...
#
# IP input is either range of class Cs, e.g 10.100.11.1-50, or defaults to looking for a local file named "ip_list" expecting an IP per line..
#
# Usage examples:  ./pyping.py 10.100.11.1-120     ||     ./pyping.py (will look in local dir for file named ip_list)
#
# Current version: 0.1 @ 12-13-2016.


import os
import sys
import subprocess
import platform
import re

os_type = platform.system()
dev_null = open(os.devnull, 'w')
good_ip = bad_ip = 0
in_data = "none"
ips = []
ip_list = []
# The following is regex to check if an ip address was supplied as an arg.
ip_pattern = re.compile(
    "^([2][0-5][0-5]|^[1]{0,1}[0-9]{1,2})\.([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})\.([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})\.([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})$")

while in_data == "none":
    if len(sys.argv) > 1:

        in_data = "cli"
        user_args = sys.argv[1]
        ip_match = re.search(ip_pattern, user_args.split("-")[0])

        if ip_match:

            ip_range = user_args.split(".")
            a = ip_range[0]
            b = ip_range[1]
            c = ip_range[2]
            d = ip_range[3]

            ip_range_d = d.split("-")
            d_start = int(ip_range_d[0])
            d_end = int(ip_range_d[1])

            index = d_start

            while index <= d_end:
                item_ip = a + "." + b + "." + c + "." + str(index)
                ips.append(item_ip)
                index += 1
    else:
        in_data = "filelist"
        try:
            ip_file = open('ip_list', 'r')
        except IOError as e:
            print(
                f"\n\n Expecting to find file named \"ip_list\" given the lack of subnet range argument. ({e.errno}): {e.strerror}\n\n")
            exit()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        for item in ip_file:
            ips.append(item)

p = {}
for ip in ips:
    if not ip.isspace():
        if os_type == "Darwin":
            p[ip] = subprocess.Popen(['ping', '-n', '-W2', '-c2', ip], stdout=dev_null, stderr=subprocess.STDOUT)
        elif os_type == "Windows":
            p[ip] = subprocess.Popen(['ping', '-w', '1000', '-n', '2', ip], stdout=dev_null, stderr=subprocess.STDOUT)
        else:
            p[ip] = subprocess.Popen(['ping', '-n', '-w2', '-c2', ip], stdout=dev_null, stderr=subprocess.STDOUT)

while p:
    for ip, proc in p.items():
        if proc.poll() is not None:
            del p[ip]
            retcode = proc.returncode
            if proc.returncode == 0:
                print('{0} active'.format(ip.rstrip()))
                good_ip += 1
            elif proc.returncode == 1:
                print('{0} no response'.format(ip.rstrip()))
                bad_ip += 1
            else:
                print('{0} returned error {1}'.format(ip.rstrip(), retcode))
                bad_ip += 1
            break

print('\nSummary:\n{} IPs responded.'.format(good_ip))
print('{} did not.'.format(bad_ip))
