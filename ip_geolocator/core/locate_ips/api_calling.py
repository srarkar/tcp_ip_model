import requests
import ip_request as req

base_request = "http://ip-api.com/json/"



def create_request(ip_addr):
    return base_request + ip_addr

def submit_requests(ips):

    
    for ip in ips:
        full_request = create_request(ip)
        response = requests.get("http://ip-api.com/json/8.8.8.8")
        header = response.headers

        data_dictionary = response.json()
        ip_request_object = req.from_dict(data_dictionary)

        
