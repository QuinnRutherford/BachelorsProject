#!/usr/bin/env python3
import os
import sys

from ts_header import TS
from scapy.all import (
    UDP,
    TCP,
    FieldLenField,
    FieldListField,
    IntField,
    IPOption,
    ShortField,
    get_if_list,
    sniff
)
from scapy.layers.inet import _IPOption_HDR

def get_if():
    ifs=get_if_list()
    iface=None
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface


recentTime = {
    'p1': 10000000,
    'p2': 10000000,
    'p3': 10000000
}

def handle_pkt(pkt):
    if UDP in pkt and pkt[UDP].dport == 1234:
        #pkt.show2()
        pathTime = pkt[TS].finalTime-pkt[TS].initTime
        recentTime['p' + str(pkt[TS].path)] = pathTime
        
        print("Path: " + str(pkt[TS].path))
        print("Raw: " + str(pkt[UDP].payload))
        print("Time (s): " + str(pathTime/1000000) + "\n")
        #print('time saved ' + str(recentTime['p' + str(pkt[TS].path)]))
        saveFastestPath()
    #    hexdump(pkt)
        sys.stdout.flush()

def saveFastestPath():
    fastestPath = 'p0'
    if recentTime['p1'] < recentTime['p2'] and recentTime['p1'] < recentTime['p3']:
        fastestPath = 'p1'
    elif recentTime['p2'] < recentTime['p1'] and recentTime['p2'] < recentTime['p3']:
        fastestPath = 'p2'
    else:
        fastestPath = 'p3'
        
    file = open('fstPath.txt', 'w')
    file.write(fastestPath)
    file.close()

def main():
    ifaces = [i for i in os.listdir('/sys/class/net/') if 'eth' in i]
    iface = ifaces[0]
    print("sniffing on %s" % iface)
    sys.stdout.flush()
    sniff(iface = iface,
          prn = lambda x: handle_pkt(x))

if __name__ == '__main__':
    main()
