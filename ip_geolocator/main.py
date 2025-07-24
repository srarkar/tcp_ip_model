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

def parse_args(argv):
    # not sure yet if sudo will be needed
    # default call: sudo python3 main.py
        # uses network sniffing + mapping
        # equivalent to sudo python3 main.py [-n] [-m]
    # with user input IPs + individual : python3 main.py -i -l 
        # prompt the user to type in IP addresses once this flag is read
    # with user input IPs + mapping: python3 main.py -i -m
        # prompt the user to type in tuples of IP addresses once this flag is read
    # consider adding .txt file reading functionality over manual input
        # python3 main.py -i -t -m ip_list.txt (user input + text file + mapping)

    # flag dictionary:
    # -n: network sniffing to get IPs (default)
    # -i: user will input IPs (either manually (default), or a .txt file (-t))
    
    network_sniffing = True # if this is false, user input is true
    mapping = True # if this is false, display only individual locations on map
    if not network_sniffing:
        manual_input = True # if this is false, then look for .txt file



def main():
    parse_args(sys.argv)
    pass

if __name__ == "__main__":
    main()