# main program logic:
    # parse arguments. currently there are six combinations of arguments
        # user input IPs + mapping (txt file or manual)
        # user input IPs + individual locations (txt file or manual)
        # network sniffed IPs + mapping
        # network sniffed IPs + individual locations

    # grab IPs from somewhere -- user input (need to validate them first) or by sniffing local network via scapy.
        # maybe also give sample IPs so user can see what tool does
    # from arguments, determine if the user wants to see individual ip locations, or mappings (arrows) from sender to dest on the map
    # call ip geolocator API on valid ip inputs
    # use Folium to display map with marked locations (red dot + text box with as speciifc a location as possible)
    # final report with number of IP addresses, and the areas visited (by country or region)

import sys
import time
from pathlib import Path

from core import handle_args as arg 
from core.obtain_ips import network_sniffing as network
from core.obtain_ips import document_handling as doc
from core.obtain_ips import user_input_ips as user

def main():
    # parse arguments and place in dictionary
    settings = arg.parse_args(sys.argv)

    # print settings based on flags, for user
    arg.print_settings(settings)
    time.sleep(1)

    ips = []

    if settings["network_sniffing"]:
        # sniff network to gather IPs
        # stop when user pressers ENTER or based on gathering a set number of IPs
        ips = network.sniff_packets(settings)
        
    elif settings["manual_input"] == False:
        # prompt the user for the path to the .txt file
        # then, parse it into IPs
        path = doc.get_doc_path(settings)
        if settings["mapping"]:
            ips = doc.parse_doc_pairs(path)
        else:
            ips = doc.parse_doc(path)

    else:
        if settings["mapping"]:
            ips = user.get_ips_mapping()
        else:
            ips = user.get_ips_location()
        
    print(ips)

    # ips have been obtained!


    sys.exit()

if __name__ == "__main__":
    main()