# given some input of IPs, process them so they're ready as input to the API
    # if the user only wants markers of IPs without mappings (sender vs dest distinction), then use a list of IP addresses
    # otherwise, use a dictionary of sender (key) to receiver (value). If a single sender has multiple destinations, append to list of values

# for individual locations: just need a frequency map for key = IP, value = how many times it appears

# for mapping: create both frequency map and keep the list of tuples.


# returns dictionary that maps IP address to how often it appears as sender or destination

def convert_to_list(ips):
    ips_list = []

    if isinstance(ips[0], tuple):
        for pair in ips:
            for ip in pair:
                ips_list.append(ip)
        return ips_list
    return ips

def generate_ip_frequencies(ips):
    ips = convert_to_list(ips)
    ip_frequencies = {}

    for ip in ips:
        if ip not in ip_frequencies:
            ip_frequencies[ip] = 1
        else:
            ip_frequencies += 1
    return ip_frequencies

