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

        ip_request_object = IPRequest.from_dict(data_dictionary)

        if header["X-Rl"] == "0":
            time.sleep(header["X-Ttl"] + 1) # wait til 45 HTTP request limit ends

        # extract info into ip request object, and store in dictionary
        if data_dictionary['status'] == 'fail':
            print(f"Failed to scout IP address {ip} due to: {data_dictionary['message']}")
            time.sleep(0.5)
            continue
        print(ip_request_object)
        if ip_request_object.lat is None or ip_request_object.long is None:
            print(f"Skipping IP {ip} due to missing location data.")
            continue
            
        ip_to_request_object[ip] = ip_request_object

    print(f"Successfully scouted the following {len(ip_to_request_object.keys())} IP(s): {', '.join(ip_to_request_object.keys())}")
    return ip_to_request_object
        
        
        
