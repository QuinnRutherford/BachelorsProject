from p4utils.mininetlib.network_API import NetworkAPI

from mininet.net import Mininet
from mininet.cli import CLI

import time
import sys

if len(sys.argv) < 3:
    print('pass 3 arguments: <delay p1(s)> <delay p2(s)> <delay p3(s)>')
    exit(1)

# delete contents of fstPath.txt
file = open('fstPath.txt', 'w').close()

net = NetworkAPI()

net.setLogLevel('info')

net.addHost('h1')
net.addHost('h2')

# S1
net.addP4RuntimeSwitch('s1')
net.setP4Source('s1', 'ts.p4')
net.setP4CliInput('s1', 's1-commands.txt')

# S2
net.addP4RuntimeSwitch('s2')
net.setP4Source('s2', 'ts.p4')
net.setP4CliInput('s2', 's2-commands.txt')

# S3
net.addP4RuntimeSwitch('s3')
net.setP4Source('s3', 'ts.p4')
net.setP4CliInput('s3', 's3-commands.txt')

# S4
net.addP4RuntimeSwitch('s4')
net.setP4Source('s4', 'ts.p4')
net.setP4CliInput('s4', 's4-commands.txt')

# S5
net.addP4RuntimeSwitch('s5')
net.setP4Source('s5', 'ts.p4')
net.setP4CliInput('s5', 's5-commands.txt')

# S6
net.addP4RuntimeSwitch('s6')
net.setP4Source('s6', 'ts.p4')
net.setP4CliInput('s6', 's6-commands.txt')

# Host Ports
#net.setIntfPort('h1', 's1', 0)
#net.setIntfPort('h2', 's2', 0)

# S1 Links & Ports
net.addLink('s1', 'h1')
net.addLink('s1', 's3')
net.addLink('s1', 's4')
net.addLink('s1', 's5')

net.setIntfPort('s1', 'h1', 1)
net.setIntfPort('s1', 's3', 3)
net.setIntfPort('s1', 's4', 4)
net.setIntfPort('s1', 's5', 5)

# S2 Links & Ports
net.addLink('s2', 'h2')
net.addLink('s2', 's3')
net.addLink('s2', 's4')
net.addLink('s2', 's6')

net.setIntfPort('s2', 'h2', 2)
net.setIntfPort('s2', 's3', 3)
net.setIntfPort('s2', 's4', 4)
net.setIntfPort('s2', 's6', 6)

# S3 Links & Ports
net.setIntfPort('s3', 's1', 1)
net.setIntfPort('s3', 's2', 2)

# S4 Links & Ports
net.setIntfPort('s4', 's1', 1)
net.setIntfPort('s4', 's2', 2)

# S5 Links & Ports
net.addLink('s5', 's6')

net.setIntfPort('s5', 's1', 1)
net.setIntfPort('s5', 's6', 6)

# S6 Links & Ports
net.setIntfPort('s6', 's2', 2)
net.setIntfPort('s6', 's5', 5)

# Delays
net.setDelay('s1', 's4', int(sys.argv[1]) * 1000) # delay on path 1
net.setDelay('s2', 's3', int(sys.argv[2]) * 1000) # delay on path 2
net.setDelay('s5', 's6', int(sys.argv[3]) * 1000) # delay on path 3

# for testing fstPath.txt
#net.setDelay('s1', 's4', 3000)

# Network Setup
net.setBwAll(5)
net.l2() # use layer 2 strategy

net.enablePcapDumpAll()
net.enableLogAll()

net.enableCli()
net.startNetwork()
