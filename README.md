# tcp_ip_model
A small collection of tools and projects concerning the Internet Protocol Stack or TCP/IP Model

<img src="https://github.com/user-attachments/assets/023aab52-8c1e-494b-bebc-3a9e56a1e6be" alt="drawing" width="500"/>

## Network Layer
### Ethernet Frame Network Sniffer
When run with ``sudo python3 arp_ip_sniffer.py``, the tool monitors your network and catches Ethernet frames, which ARP or IP packets. The tool parses these packets to determine the sender and destination IP Address/ MAC Address. It also keeps an eye out for potential ARP Spoofing, IP Spoofing, or DDoS attack, by checking mappings between IP and MAC addresses, and the number of times a certain IP address is the sender or receiver of a packet on the current network.
