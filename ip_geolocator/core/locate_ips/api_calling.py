import requests
import time
from .ip_request import IPRequest

base_request = "http://ip-api.com/json/"

def submit_requests(ips):
    ip_to_request_object = {}
    for ip in ips:
        response = requests.get(base_request + ip)
        header = response.headers
        data_dictionary = response.json()

        # extract info into ip request object, and store in dictionary
        if data_dictionary['status'] == 'fail':
            print(f"Failed to scout IP address {ip} due to: {data_dictionary['message']}")
            time.sleep(0.5)
            continue
        ip_request_object = IPRequest.from_dict(data_dictionary)
        ip_to_request_object[ip] = ip_request_object

        if header["X-Rl"] == 0:
            time.sleep(header["X-Ttl"] + 1)
            # wait til 45 HTTP request limit ends
    time.sleep(0.5)
    print(f"Successfully scouted the following {len(ip_to_request_object.keys())} IPs: {', '.join(ip_to_request_object.keys())}")
    return ip_to_request_object
        
        
        
