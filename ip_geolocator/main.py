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
from core import network_sniffing as network


def main():
    # parse arguments and place in dictionary
    settings = arg.parse_args(sys.argv)

    # print settings based on flags, for user
    arg.print_settings(settings)

    ips = []

    if settings["network_sniffing"]:
        # sniff network to gather IPs
        # stop when user pressers ENTER or based on gathering a set number of IPs
        network.sniff_packets()

    elif settings["manual_input"] == False:
        # look for .txt file and parse it into IPs
        pass
    else:
        # ask user to input IPs manually. first, check if mapping is true. if it is, ask for pairs of sender and destination. 
        # otherwise, just get one IP at a time
        pass

    sys.exit()

if __name__ == "__main__":
    main()