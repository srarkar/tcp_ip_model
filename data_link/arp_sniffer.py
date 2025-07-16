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


interfaces = netifaces.interfaces()

os = platform.uname().system
match os:
    case "Darwin":
        print("Detected OS: MacOS / Darwin")
        # Use "en0" for Ethernet/WiFi frames
    case "Linux":
        print("Detected OS: Linux")
        # Use "eth*" for ethernet and "wlan*" for WiFi
    case "Windows":
        print("Detected OS: Windows")
        # Npcap?
    case _:
        raise NotImplementedError("Unsupported or unknown operating system.")
    
    
# using scapy, open a capture handle on interface "en0"
# apply "arp" filter -- access frame[Ether].type and check if it is equal to x0806 (ARP)
# parse delivered packet, originally a buffer of raw bytes
ip_to_mac = {}
while(True):
    packets = scapy.sniff(count=1)
    current_frame = packets[0]
    if current_frame["Ether"].type == EtherType.ARP.value: # ARP Packet

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
            
                affirmatives = {"yes", "ye", "yurr", "yeah", "indeed"}
                print(f"Continue sniffing?")
                check_continue = input()
                if check_continue in affirmatives:
                    continue
                else:
                    break

        time.sleep(0.25)
    elif current_frame["Ether"].type == EtherType.IPv4.value: # IPv4 packet
        print("IPv4 Packet Found")
        # print(current_frame)
    # time.sleep(0.5) # read a packet every half second