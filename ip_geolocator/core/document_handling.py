import os
import sys
from pathlib import Path
# request document path from user, 
def get_doc_path(settings):
    if settings["mapping"]:
        print(f"IP addresses should be formatted in the format of sender_ip, destination_ip, with one pair per line.")
    else:
        print(f"The document be formatted with one IP address on its own line.")
    
    num_tries = 5
    while (num_tries > 0):
        path = input("Provide the path of the document containing the IP addresses here: ")
        if not os.path.isfile(path):
            print(f"Provided path does not lead to a file. Please try again.")
            num_tries -= 1
            continue
        break
    if num_tries == 0:
        print(f"Too many tries.")
        sys.exit()
    
    # TODO: make this a while loop
    if Path(path).suffix != ".txt":
        print("Ensure document is a .txt file")
    return path

# parse document, expecting individual IPs only
def parse_doc(path):
    with open(path, 'r') as f:
        ips = []
        for line_num, line in enumerate(f, start=1):
            ip = line.strip()
            if ip:
                try:
                    if validate_ip_addr(ip):
                        ips.append(ip)
                    else:
                        print(f"Line {line_num}: Invalid IP format: '{ip}'")
                except Exception as e:
                    print(f"Line {line_num}: Error parsing line: {e}")
    print(f"{len(ips)} IP addresses successfully parsed.")
    return ips

# parse expecting tuples of IPs (sender, destination)
def parse_doc_pairs(file_path):
    ip_pairs = []
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue  # skip empty lines
            try:
                parts = [part.strip() for part in line.split(',')]
                if len(parts) != 2:
                    print(f"Line {line_num}: Invalid format, expected 2 IPs separated by a comma.")
                    continue
                sender_ip, dest_ip = parts
                if validate_ip_addr(sender_ip) and validate_ip_addr(dest_ip):
                    ip_pairs.append((sender_ip, dest_ip))
                elif validate_ip_addr(sender_ip):
                    print(f"Line {line_num}: Invalid IP format: '{dest_ip}'")
                elif validate_ip_addr(dest_ip):
                    print(f"Line {line_num}: Invalid IP format: '{sender_ip}'")
                else:
                    print(f"Line {line_num}: Invalid IP format: '{sender_ip}', '{dest_ip}'")

            except Exception as e:
                print(f"Line {line_num}: Error parsing line: {e}")
    print(f"{len(ip_pairs)} IP address pairs successfully obtained.")
    return ip_pairs

def validate_ip_addr(ip_addr):
    parts = ip_addr.strip().split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
    return True
