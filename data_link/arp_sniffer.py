# looks at ARP packets sent on LAN, check MAC/IP pairs
# how to utilize ethernet frame structure??

import netifaces
import scapy.all as scapy
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

while(True):
    packets = scapy.sniff(count=1)
    current_frame = packets[0]
    if current_frame["Ether"].type == EtherType.ARP.value: # ARP Packet
        print("ARP Packet")
        print(f"Sender MAC Address: {current_frame['ARP'].hwsrc}")
        print(f"Sender IP Address: {current_frame['ARP'].psrc}")
        break
    elif current_frame["Ether"].type == EtherType.IPv4.value: # IPv4 packet
        pass
        # print("IPv4 Packet")
        # print(current_frame)
    # time.sleep(0.5) # read a packet every half second