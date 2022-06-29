
from scapy.all import *

TYPE_TS = 0x1212
TYPE_IPV4 = 0x0800

class TS(Packet):
    name = "ts"
    fields_desc = [
        ShortField("pid", 0),
        ShortField("path", 0),
        BitField("initTime", 0, 48),
        BitField("finalTime", 0, 48)
    ]
    def mysummary(self):
        return self.sprintf("pid=%pid%, initTime=%initTime%, finalTime=%finalTime%")
        #path=%path%,
        
bind_layers(Ether, TS, type=TYPE_TS)
bind_layers(TS, IP, pid=TYPE_IPV4)