# looks at ARP packets sent on LAN, check MAC/IP pairs
# how to utilize ethernet frame structure??

import netifaces
import scapy.all as scapy
import platform
import time


interfaces = netifaces.interfaces()

os = platform.uname().system
match os:
    case "Darwin":
        print("MacOS")
        # Use "en0" for Ethernet/WiFi frames
    case "Linux":
        print("Linux")
        # Use "eth*" for ethernet and "wlan*" for WiFi
    case "Windows":
        print("Windows")
        # Npcap?
    case _:
        raise NotImplementedError("Unsupported or unknown operating system.")
    
# using scapy, open a capture handle on interface "en0"
# apply "arp" filter -- access frame[Ether].type and check if it is equal to x0806 (ARP)
# parse delivered packet, originally a buffer of raw bytes

while(True):
    packets = scapy.sniff(count=1)
    current_frame = packets[0]
    if current_frame["Ether"].type == 2054: # ARP Packet
        print("ARP Packet found")
        print(current_frame.summary)
    elif current_frame["Ether"].type == 2048: # IPv4 packet
        print("IPv4 Packet")
        print(current_frame.summary)
    time.sleep(0.5) # read a packet every half second