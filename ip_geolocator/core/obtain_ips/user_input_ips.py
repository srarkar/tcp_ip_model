# get manually typed IP addresses
from core.obtain_ips import document_handling as doc

affirmatives = {"yes", "ye", 'y', "yurr", "yeah", "yup", "indeed"}
negatives = {"no", "n", "no thanks", "naw", "nope", "stop", "quit", "done"}


def get_ips_location():
    # loop until the user types a key phrase to stop? every 10 IPs ask if the user wants to stop here
    print("Enter in IP addresses one at a time.")
    print("Type 'stop' or 'no' at any point to stop inputting IPs")
    ips = []

    while (True):
        if len(ips) % 20:
            stop = input(f"{len(ips)} IP addresses have been obtained. Stop now?")
            if stop.lower() in affirmatives:
                break
        ip = input(f"Please type IP address #{len(ips) + 1}: ")
        if ip in negatives:
            break
        if doc.validate_ip_addr(ip):
            ips.append(ip)
        else:
            print(f"Invalid IP address entered: {ip}.")

    if len(ips) == 1:
        print(f"{len(ips)} IP address obtained successfully")
    else:
        print(f"{len(ips)} IP addresses obtained successfully")
    return ips

def get_ips_mapping():
    print("When prompted, enter sender IP address, followed by the desination IP address.")
    print("Type 'stop' or 'no' at any point to stop inputting IPs")
    ips = []

    while (True):
        sender_ip = input(f"Please enter source IP address #{len(ips) + 1}: ")
        destination_ip = input(f"Please enter destination IP address #{len(ips) + 1}: ")
        if sender_ip.lower() in negatives or destination_ip.lower() in negatives:
            print(f"Done entering IPs.")
            break
        if doc.validate_ip_addr(sender_ip) and doc.validate_ip_addr(destination_ip):
            ips.append((sender_ip, destination_ip))
        elif doc.validate_ip_addr(sender_ip):
            print(f"Invalid destination IP address entered: {destination_ip}.")
        elif doc.validate_ip_addr(destination_ip):
            print(f"Invalid source IP address entered: {sender_ip}.")
        else: # both are invalid
            print(f"Invalid source and destination IP addresses entered: {sender_ip}, {destination_ip}")

    print(f"{len(ips)} IP address pair(s) obtained successfully")
    return ips