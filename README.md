# tcp_ip_model
A small collection of tools and projects concerning the Internet Protocol Stack or TCP/IP Model

<img src="https://github.com/user-attachments/assets/023aab52-8c1e-494b-bebc-3a9e56a1e6be" alt="drawing" width="500"/>

## Network Layer
### Ethernet Frame Network Sniffer
When run, this tool monitors your network and catches Ethernet frames, which ARP or IP packets. The tool parses these packets to determine the sender and destination IP Address/ MAC Address. It also keeps an eye out for potential ARP Spoofing, IP Spoofing, or DDoS attack, by checking mappings between IP and MAC addresses, and the number of times a certain IP address is the sender or receiver of a packet on the current network.

#### Usage
**THIS NEEDS TO BE UPDATED**
##### MacOS/Linux
  - Once you have forked the repository, ``cd`` into the directory named "data_link", in reference to the layer of the Internet Protocol Stack the tool interacts with most.
  - From there, run ``source .venv/bin/activate`` to activate the virtual environment.
  - Next, install the necessary dependencies by running ``pip install -r requirements.txt`` since the tool utilizes the ``netifaces`` and ``scapy`` packages which are third-party libraries.
  - Lastly, simply run the tool with ``sudo python3 arp_ip_sniffer.py``. Root permission (sudo) will likely be necessary to have the privilege to view network traffic. 
##### Windows
  - Once you have forked the repository, ``cd`` into the directory named "data_link", in reference to the layer of the Internet Protocol Stack the tool interacts with most.
  - From there, run ``.venv\Scripts\activate.bat`` (cmd) or ``.venv\Scripts\Activate.ps1`` (PowerShell) to activate the virtual environment.
  - Next, install the necessary dependencies by running ``pip install -r requirements.txt`` since the tool utilizes the ``netifaces`` and ``scapy`` packages which are third-party libraries.
  - Lastly, run the tool with ``python arp_ip_sniffer.py``

## Internet Layer
### IP Geolocator
When run, this tool collects IP addresses from a user-specified source, which can be from network sniffing, manual typing, or saved in a separate text document. It then plots them on a graph to visually represent where packets are coming and going from.
