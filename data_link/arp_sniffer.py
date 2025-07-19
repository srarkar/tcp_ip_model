# looks at ARP packets sent on LAN, check MAC/IP pairs
# how to utilize ethernet frame structure??

import netifaces
import scapy.all as scapy
from scapy.all import Ether, ARP
import platform

import time
import sys
import select
from enum import Enum

class EtherType(Enum):
    IPv4 = 2048
    ARP = 2054

affirmatives = {"yes", "ye", 'y', "yurr", "yeah", "yup", "indeed"}
negatives = {"no", "n", "no thanks", "naw", "nope", "stop", "quit"}

def print_report(num_arp_packets, num_ip_packets, malicious_ips, malicious_macs):
    print("Summary of Network Sniffing:")
    print(f"\tNumber of packets sniffed: {num_arp_packets + num_ip_packets}")
    print(f"\tNumber of ARP Packets: {num_arp_packets}")
    print(f"\tNumber of IPv4 Packets: {num_ip_packets}")
    if malicious_ips:
        print(f"\tPotential ARP Spoofing at the following IP Addresses: {', '.join(malicious_ips)}")
    if malicious_macs:
        print(f"\tPotential IP Spoofing at the following MAC Addresses: {', '.join(malicious_macs)}")

def detect_enter_keypress():
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline()
        if line.strip() == "":
            return True
    return False


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

malicious_ip = set()
malicious_mac = set()

num_arp_packets = 0
num_ip_packets = 0

print("Commencing network sniffing...")

with open('nose_ascii.txt', 'r') as file:
    for line in file:
        print(line.strip())

print("Press ENTER at any point to terminate execution")

while(True):
    packets = scapy.sniff(count=1, iface = iface)
    current_frame = packets[0]
    if detect_enter_keypress():
        break
    if current_frame["Ether"].type == EtherType.ARP.value: # ARP Packet
        num_arp_packets += 1
        # Access fields and place into locals
        sender_mac_addr = current_frame['ARP'].hwsrc
        sender_ip_addr = current_frame['ARP'].psrc

        dest_mac_addr = current_frame['ARP'].hwsrc
        dest_ip_addr = current_frame['ARP'].pdst

        # print fields
        print("ARP Packet Found")

        print(f"\tSender IP Address: {sender_ip_addr}")
        print(f"\tSender MAC Address: {sender_mac_addr}")

        print(f"\tDestination IP Address: {dest_ip_addr}")
        print(f"\tDestination MAC Address: {dest_mac_addr}")

        # maintain dictionary of ip addrs mapped to MAC addresses
        if sender_ip_addr not in ip_to_mac:
            ip_to_mac[sender_ip_addr] = {sender_mac_addr}
        else:
            # found multiple mac addresses mapped to the same IP, possible ARP spoofing
            if sender_mac_addr not in ip_to_mac[sender_ip_addr]:
                ip_to_mac[sender_ip_addr].add(sender_mac_addr)
                print(f"Multiple MAC addresses have been detected as mapped to the same IP.")
                print(f"For IP address {sender_ip_addr}, the following MAC address mappings have been detected:")
                for hwsrc in ip_to_mac[sender_ip_addr]:
                    print("\t" + hwsrc)

                malicious_ip.add(sender_ip_addr)


                # at this point, we've found a potential case of ARP Spoofing
                # provide user choice to continue sniffing or break early
                affirmatives = {"yes", "ye", 'y', "yurr", "yeah", "yup", "indeed"}
                negatives = {"no", "n", "no thanks", "naw", "nope", "stop", "quit"}
                print(f"Continue sniffing?")
                exit_now = False
                while(True):
                    check_continue = input()
                    if check_continue in affirmatives:
                        break
                    elif check_continue in negatives:
                        exit_now = True
                        break
                    else:
                        print("Please answer yes or no.")

                if exit_now: 
                    break
    elif current_frame["Ether"].type == EtherType.IPv4.value: # IPv4 packet
        num_ip_packets += 1
        print("IPv4 Packet Found")
        # TODO: add some prints here for IP packet fields
    if detect_enter_keypress():
        break
    time.sleep(0.1)

print_report(num_arp_packets, num_ip_packets, malicious_ip, malicious_mac)


