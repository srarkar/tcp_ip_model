# main program logic:
    # parse arguments. currently there are four combinations of arguments
        # user input IPs + mapping
        # user input IPs + individual locations
        # network sniffed IPs + mapping
        # network sniffed IPs + individual locations
    # grab IPs from somewhere -- user input (need to validate them first) or by sniffing local network via scapy.
        # maybe also give sample IPs so user can see what tool does
    # from arguments, determine if the user wants to see individual ip locations, or mappings (arrows) from sender to dest on the map
    # call ip geolocator API on valid ip inputs
    # use Folium to display map with marked locations (red dot + text box with as speciifc a location as possible)
    # final report with number of IP addresses, and the areas visited (by country or region)