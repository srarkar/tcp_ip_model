# looks at ARP packets sent on LAN, check MAC/IP pairs
# how to utilize ethernet frame structure??

import netifaces
import scapy.all as scapy
from scapy.all import Ether, ARP
import platform
import time
from enum import Enum

class EtherType(Enum):
    IPv4 = 2048
    ARP = 2054

def print_report(num_arp_packets, num_ip_packets):
    print(f"Number of packets sniffed: {num_arp_packets + num_ip_packets}")
    print(f"Number of ARP Packets: {num_arp_packets}")
    print(f"Number of IPv4 Packets: {num_ip_packets}")
    print(f"Potential ARP Spoofing at the following IP Addresses: {list(malicious_ip)}")
    print(f"Potential IP Spoofing at the MAC Addresses: ")

interfaces = netifaces.interfaces()

os = platform.uname().system
match os:
    case "Darwin":
        print("Detected OS: MacOS / Darwin")
        iface = "en0"
    case "Linux":
        print("Detected OS: Linux")
        iface = "eth0"
    case "Windows":
        print("Detected OS: Windows")
        iface = "Ethernet"
    case _:
        raise NotImplementedError("Unsupported or unknown operating system.")
    
    
# using scapy, open a capture handle on interface "en0"
# apply "arp" filter -- access frame[Ether].type and check if it is equal to x0806 (ARP)
# parse delivered packet, originally a buffer of raw bytes
ip_to_mac = {}
mac_to_ip = {}

malicious_ip = {}
malicious_mac = {}

num_arp_packets = 0
num_ip_packets = 0
while(True):
    packets = scapy.sniff(count=1, iface = iface)
    current_frame = packets[0]
    if current_frame["Ether"].type == EtherType.ARP.value: # ARP Packet
        num_arp_packets += 1
        # Access fields and place into locals
        sender_mac_addr = current_frame['ARP'].hwsrc
        sender_ip_addr = current_frame['ARP'].psrc

        # dest_mac_addr = 
        # dest_ip_addr = 


        print("ARP Packet Found")
        print(f"Sender IP Address: {sender_ip_addr}")
        print(f"Sender MAC Address: {sender_mac_addr}")
        if sender_ip_addr not in ip_to_mac:
            ip_to_mac[sender_ip_addr] = {sender_mac_addr}
        else:
            if sender_mac_addr not in ip_to_mac[sender_ip_addr]:
                ip_to_mac[sender_ip_addr].add(sender_mac_addr)
                print(f"Multiple MAC addresses have been detected as mapped to the same IP.")
                print(f"For IP address {sender_ip_addr}, the following MAC address mappings have been detected:")
                for hwsrc in ip_to_mac[sender_ip_addr]:
                    print("\t" + hwsrc)

                malicious_ip.add(sender_ip_addr)

                affirmatives = {"yes", "ye", 'y', "yurr", "yeah", "indeed"}
                print(f"Continue sniffing?")
                check_continue = input()
                if check_continue in affirmatives:
                    continue
                else:
                    break
    elif current_frame["Ether"].type == EtherType.IPv4.value: # IPv4 packet
        num_ip_packets += 1
        print("IPv4 Packet Found")
        # TODO: add some prints here for IP packet fields
    


    time.sleep(0.25)
print_report(num_arp_packets, num_ip_packets, malicious_ip, malicious_mac)