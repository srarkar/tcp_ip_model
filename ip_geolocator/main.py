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

from utils import handle_args as arg 
from utils import process_ips as process
from core.obtain_ips import network_sniffing as network
from core.obtain_ips import document_handling as doc
from core.obtain_ips import user_input_ips as user
from core.locate_ips import api_calling as api
from core.plot_ips import plot

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

        # TODO: can move the if-else logic into document_handling.
        ips = doc.parse_doc(path, settings["mapping"])

    else:
        ips = user.get_ips(settings["mapping"])


    if not ips:
        print("No IP addresses obtained. Exiting...")
        sys.exit()

    # ips have been obtained!

    ip_frequencies = process.generate_ip_frequencies(ips)

    # frequency map of IP addresses obtained!

    # make api requests for each ip in the frequency map
    ip_to_request_object = api.submit_requests(ip_frequencies.keys())
    
    # now, we have information for each IP, as well as their frequencies. 
    
    # TODO: need list of tuples of ip request object pairs 
    # for each tuple in ips, check value using ip as key
    ip_request_pairs = []
    if settings["mapping"]:
        for ip in ips:
            ip_request_pairs.append((ip_to_request_object[ip[0]], ip_to_request_object[ip[1]]))
            

    plot.plot_ips_on_map(ip_to_request_object.values(), ip_frequencies, ip_request_pairs)

    sys.exit()

if __name__ == "__main__":
    main()
