# handle flags, settings

def parse_args(argv):
    ## not sure yet if sudo will be needed
    # default call: sudo python3 main.py
        # uses network sniffing + mapping
        # equivalent to sudo python3 main.py [-n] [-m]
    # with user input IPs + individual : python3 main.py -i -l 
        # prompt the user to type in IP addresses once this flag is read
    # with user input IPs + mapping: python3 main.py -i -m
        # prompt the user to type in tuples of IP addresses once this flag is read
    # consider adding .txt file reading functionality over manual input
        # python3 main.py -i -d -m ip_list.txt (user input + text file + mapping)

    # flag dictionary:
    # -n: network sniffing to get IPs (default)
    # -i: user will input IPs (either manually (default), or a .txt file (-t))
    # -m: mapping. map displays arrow from sender to destination (default)
    # -l: map will only display individual locations
    # -d for document/text file IP input
    # -t for manually type input
    settings_map = {}

    flags = set(argv[1:])
    
    # network sniffing vs user input
    if "-n" in flags and ("-t" in flags or "-d" in flags):
        print("The tool only accepts IP addresses from a single source: network sniffing or manual input. Double check the flags used and try again.")
        sys.exit()
    elif "-t" in flags or "-d" in flags:

        network_sniffing = False # if this is false, user input is true

        if "-t" in flags and "-d" in flags:
            print("The flags '-t' and '-d' cannot coexist -- choose either to type IPs manually or keep them in a separate text file. Please try again.")
            sys.exit()
        elif "-t" in flags:
            manual_input = True
            flags.discard("-t")
        elif "-d" in flags:
            manual_input = False # look for text file input
            flags.discard("-d")

    elif "-n" in flags:
        network_sniffing = True
        manual_input = None
        flags.discard("-n")

    else:
        network_sniffing = True # default
        manual_input = None

    # mapping from sender to dest, or just individual location markers
    if "-m" in flags and "-l" in flags:
        print("The flags '-m' and '-l' cannot coexist. Please try again.")
        sys.exit()
    elif "-m" in flags:
        mapping = True
        flags.discard("-m")
    elif "-l" in flags:
        mapping = False
        flags.discard("-l")
    else:
        mapping = True # default

    if flags:
        print(f"One or more invalid flags have been detected. They have been ignored.")
    
    settings_map["network_sniffing"] = network_sniffing
    settings_map["manual_input"] = manual_input
    settings_map["mapping"] = mapping
    return settings_map

def print_settings(settings):
    if settings["network_sniffing"]:
        ip_addr_src = "network sniffing"
    elif settings["manual_input"]:
        ip_addr_src = "manual typing"
    else:
        ip_addr_src = "a separate text document"
    
    print(f"IP addresses will be obtained from {ip_addr_src}")
    
    if settings["mapping"]:
        print(f"Map will display connections between source and destination IPs")
    else:
        print(f"Map will only display individual locations, without connections")
    return