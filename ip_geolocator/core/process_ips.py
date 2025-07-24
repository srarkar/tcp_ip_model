# given some input of IPs, process them so they're ready as input to the API
    # if the user only wants markers of IPs without mappings (sender vs dest distinction), then use a list of IP addresses
    # otherwise, use a dictionary of sender (key) to receiver (value). If a single sender has multiple destinations, append to list of values
    # use parsed args to choose between them

