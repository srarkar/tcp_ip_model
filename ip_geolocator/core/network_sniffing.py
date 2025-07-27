from pathlib import Path
import time
import sys
import select

import netifaces
import os

import scapy.all as scapy

import platform


def detect_enter_keypress():
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline()
        if line.strip() == "":
            return True
    return False

interfaces = netifaces.interfaces()

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



def start_sniffing():
    nose_ascii = Path(__file__).resolve().parent.parent.parent / "shared_files" / "nose_ascii.txt"
        
    print("Commencing network sniffing...")

    with open(nose_ascii, 'r') as file:
        for line in file:
            print(line.strip())

    print("Press ENTER at any point to terminate execution")

def sniff_packets():

    print("How many packets should be sniffed?\nNote that the number of IP addresses found will be double the number of sniffed packets.")
    while True:
        try:
            total_packets = int(input("Enter number of packets: "))
            if total_packets <= 0:
                print("Number of packets must be greater than 0.")
                continue
            break
        except ValueError:
            print("Number of packets must be a positive integer. Please try again.")

    start_sniffing()
    time.sleep(1)

    packets = []
    num_packets = 0

    # store tuples of (sender_ip, dest_ip)
    while num_packets < total_packets:
        if detect_enter_keypress():
            print(f"{num_packets} packets successfully sniffed")
            return packets
        
        sniffed_packet = scapy.sniff(count=1, iface = iface, filter="ip")
        current_packet = sniffed_packet[0]
        
        num_packets += 1

        source_ip = current_packet["IP"].src
        destination_ip = current_packet["IP"].dst

        print(f"Packet #{num_packets} sniffed.")
        print(f"\tSource IP: {source_ip}")
        print(f"\tDestination IP: {destination_ip}")

        packets.append((source_ip, destination_ip))

        time.sleep(0.25)
    print(f"{num_packets} packets successfully sniffed")
    return packets
