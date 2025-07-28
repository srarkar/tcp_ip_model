import os
import sys
from pathlib import Path
# request document path from user, 
def get_doc_path(settings):
    if settings["mapping"]:
        print(f"IP addresses should be formatted as tuples in the format of (sender_ip, destination_ip)")
    else:
        print(f"The document be formatted as whitespace-separated IP addresses")
    
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
        print("Ensure document suffix is .txt")
    return path

