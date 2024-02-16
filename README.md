Simple parallel ipv4 ping library / cli utility.

Cli accepts ip range input, e.g. 10.10.10.1-255, and returns 2 lists, responding and non-responding ips

This originated from need to quick-check many IPs after disaster-recovery excercises.
intended to be moldable, and propably offers most of its value as an example of
using python lists in unusual ways :)

Sample usage scanning 192.168.0.1/30:

    Python 3.9.6 (default, Nov 10 2023, 13:38:27) 
    [Clang 15.0.0 (clang-1500.1.0.2.5)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import parping
    >>> p = parping.Parping()
    >>> p.parping_range('192.168.0.1','30')
    parsing 192.168.0.1/30
    prepinging 192.168.0.0
    Darwin/MacOS detected..
    Adding 192.168.0.0 to iplist..
    prepinging 192.168.0.1
    Darwin/MacOS detected..
    Adding 192.168.0.1 to iplist..
    prepinging 192.168.0.2
    Darwin/MacOS detected..
    Adding 192.168.0.2 to iplist..
    prepinging 192.168.0.3
    Darwin/MacOS detected..
    Adding 192.168.0.3 to iplist..
    192.168.0.1 active
    192.168.0.0 returned error
    192.168.0.3 returned error
    192.168.0.2 returned error
    
    Summary:
    1 responding IPs.
    3 non-responding IPs
    (1, 3)
    >>> 
