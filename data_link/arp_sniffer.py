# looks at ARP packets sent on LAN, check MAC/IP pairs
# how to utilize ethernet frame structure??

import netifaces
import platform

interfaces = netifaces.interfaces()

os = platform.uname().system
match os:
    case "Darwin":
        print("MacOS")
        # Use "en0" for Ethernet/WiFi frames
    case "Linux":
        print("Linux")
        # Use "eth*" for ethernet and "wlan*" for WiFi
    case "Windows":
        print("Windows")
        # Npcap?
    case _:
        raise NotImplementedError("Unsupported or unknown operating system.")