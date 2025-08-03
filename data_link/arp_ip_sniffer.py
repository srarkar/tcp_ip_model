import scapy.all as scapy
from scapy.all import Ether, ARP
import platform
import os

import time
import sys
import select
from enum import Enum

from pathlib import Path

class EtherType(Enum):
    IPv4 = 2048
    ARP = 2054

MAX_IP = 500

affirmatives = {"yes", "ye", 'y', "yurr", "yeah", "yup", "indeed"}
negatives = {"no", "n", "no thanks", "naw", "nope", "stop", "quit"}

def continue_or_break():
    limit = 5

    while(True):
        check_continue = input()
        if check_continue in affirmatives:
            return False
        elif check_continue in negatives:
            return True
        else:
            if limit <= 0:
                print("Too many invalid attempts. Exiting...")
                return False
            print("Please answer yes or no.")
            limit -= 1

def detect_enter_keypress():
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline()
        if line.strip() == "":
            return True
    return False

def print_report(num_arp_packets, num_ip_packets, malicious_ips, ddos_ip_send, ddos_ip_dest):
    print("Summary of Network Sniffing:")
    print(f"\tNumber of packets sniffed: {num_arp_packets + num_ip_packets}")
    print(f"\tNumber of ARP Packets: {num_arp_packets}")
    print(f"\tNumber of IPv4 Packets: {num_ip_packets}")
    if malicious_ips:
        print(f"\tPotential ARP Spoofing at the following IP Addresses: {', '.join(malicious_ips)}")
    if ddos_ip_send:
        print(f"\tPotential DDoS Attack from following IP Addresses: {', '.join(ddos_ip_send)}")
    if ddos_ip_dest:
        print(f"\tPotential DDoS Victim at following IP Addresses: {', '.join(ddos_ip_dest)}")


operating_system = platform.uname().system
match operating_system:
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
    
if operating_system != "Windows" and os.geteuid() != 0:
    print("Warning: You may need to run this script with sudo / root permission.")

    
    
# using scapy, open a capture handle on interface "en0"
# apply "arp" filter -- access frame[Ether].type and check if it is equal to x0806 (ARP)
# parse delivered packet, originally a buffer of raw bytes
ip_to_mac = {}
seen_sender_ips = {}
seen_dest_ips = {}

malicious_ips = set()
ddos_ip_send = set()
ddos_ip_dest = set()

num_arp_packets = 0
num_ip_packets = 0

nose_ascii = Path(__file__).resolve().parent.parent / "shared_files" / "nose_ascii.txt"

print("Commencing network sniffing...")

with open(nose_ascii, 'r') as file:
    for line in file:
        print(line.strip())

print("Press ENTER at any point to terminate execution")

start_time = time.time()
while(True):
    packets = scapy.sniff(count=1, iface = iface)
    current_frame = packets[0]
    if detect_enter_keypress(): # check if user wants to terminate execution
        break
    if current_frame["Ether"].type == EtherType.ARP.value: # ARP Packet

        # Access fields and place into locals
        sender_mac_addr = current_frame['ARP'].hwsrc
        sender_ip_addr = current_frame['ARP'].psrc

        dest_mac_addr = current_frame['ARP'].hwdst
        dest_ip_addr = current_frame['ARP'].pdst

        # print fields
        print("ARP Packet Found")

        print(f"\tSender IP Address: {sender_ip_addr}")
        print(f"\tSender MAC Address: {sender_mac_addr}")

        print(f"\tDestination IP Address: {dest_ip_addr}")
        print(f"\tDestination MAC Address: {dest_mac_addr}\n")

        num_arp_packets += 1

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

                malicious_ips.add(sender_ip_addr)

                # at this point, we've found a potential case of ARP Spoofing
                # provide user choice to continue sniffing or break early
                limit = 5
                print(f"You may continue sniffing or break to view network summary and investigate potential ARP Spoofing")
                time.sleep(0.1)
                print(f"Continue sniffing?")

                exit_now = continue_or_break()
                if exit_now:
                    break

    elif current_frame["Ether"].type == EtherType.IPv4.value: # IPv4 packet
        protocol = None
        # Access fields and place into locals
        sender_ip = current_frame["IP"].src
        if sender_ip in seen_sender_ips:
            seen_sender_ips[sender_ip] += 1
        else:
            seen_sender_ips[sender_ip] = 1

        dest_ip = current_frame["IP"].dst
        if dest_ip in seen_dest_ips:
            seen_dest_ips[dest_ip] += 1
        else:
            seen_dest_ips[dest_ip] = 1
    


        if current_frame.getlayer(scapy.TCP):
            protocol = "TCP"
        elif current_frame.getlayer(scapy.UDP):
            protocol = "UDP"


        print("IPv4 Packet Found")
        print(f"\tSender IP Address: {sender_ip}")
        print(f"\tDestination IP Address: {dest_ip}")
        if protocol:
            print(f"\tProtocol: {protocol}\n")
        
        num_ip_packets += 1
        sent_found = False
        dest_found = False

        if time.time() - start_time >= 30:
            start_time = time.time()
            for ip, freq in seen_sender_ips.items():
                if freq > MAX_IP:
                    ddos_ip_send.add(ip)
                    sent_found = True
            for ip, freq in seen_dest_ips.items():
                if freq > MAX_IP:
                    ddos_ip_dest.add(ip)
                    dest_found = True
            seen_sender_ips = {}
            seen_dest_ips = {}

            if sent_found:
                print(f"Over 1000 packets per minute have been detected being sent from at least one IP Address.")
            
            if dest_found:
                print(f"Over 1000 packets per minute have been detected being sent to a single IP Address, a potential sign of a DDoS attack.")

            # provide user choice to continue sniffing or break early
            if sent_found or dest_found:
                print(f"You may continue sniffing or break to view network summary and investigate potential IP spoofing or DDoS attack")
                time.sleep(0.1)
                print(f"Continue sniffing? Please say 'yes' or 'no'")

                continue_sniffing = continue_or_break()
                if continue_sniffing:
                    break

    if detect_enter_keypress():
        break

print_report(num_arp_packets, num_ip_packets, malicious_ips, ddos_ip_send, ddos_ip_dest) # final report from sniffing


