#!/usr/bin/env python3
import random
import socket
import sys

from ts_header import TS
from scapy.all import IP, UDP, TCP, Ether, get_if_hwaddr, get_if_list, sendp

def get_if():   # get eth0
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface

def main():

    if len(sys.argv)<3:
        print('pass 3 arguments: <destination> "<message>"')
        exit(1)

    addr = socket.gethostbyname(sys.argv[1])
    iface = get_if()

    print("sending on interface %s to %s" % (iface, str(addr)))
    
    if len(sys.argv) == 3:
        for i in range(3):
            pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
            pkt = pkt / TS(pid=0x800, path=i+1) /  IP(dst=addr) / UDP(dport=1234, sport=random.randint(49152,65535)) / sys.argv[2]
            #pkt.show2()
            sendp(pkt, iface=iface, verbose=False)
    
    if len(sys.argv) == 4:
        pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
        pkt = pkt / TS(pid=0x800, path=int(sys.argv[3])) /  IP(dst=addr) / UDP(dport=1234, sport=random.randint(49152,65535)) / sys.argv[2]
        #pkt.show2()
        sendp(pkt, iface=iface, verbose=False)


if __name__ == '__main__':
    main()
