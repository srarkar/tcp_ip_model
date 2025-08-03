import requests
import time
from .ip_request import IPRequest

base_request = "http://ip-api.com/json/"



def create_request(ip_addr):
    return base_request + ip_addr

def submit_requests(ips):

    ip_to_request_object = {}
    for ip in ips:
        full_request = create_request(ip)
        response = requests.get(full_request)
        header = response.headers
        data_dictionary = response.json()

        # extract info into ip request object, and store in dictionary
        if data_dictionary['status'] == 'fail':
            print(f"Failed to scout IP address {ip} because of: {data_dictionary['message']}")
            time.sleep()
        ip_request_object = IPRequest.from_dict(data_dictionary)
        ip_to_request_object[ip] = ip_request_object

        if header["X-Rl"] == 0:
            time.sleep(header["X-Ttl"] + 1)
            # wait til 45 HTTP request limit ends
    return ip_to_request_object
        
        
        
