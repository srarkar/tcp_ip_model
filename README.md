# tcp_ip_model

A small collection of tools and projects concerning the Internet Protocol Stack (TCP/IP Model).

<img src="https://github.com/user-attachments/assets/023aab52-8c1e-494b-bebc-3a9e56a1e6be" alt="drawing" width="500"/>

The projects begin at the data link layer and work their way up to TCP sockets and HTTP requests.

---

## Directory Structure

```
tcp_ip_model/
├── .venv/                # Python virtual environment
├── data_link/
│   └── arp_ip_sniffer.py
├── ip_geolocator/
│   ├── main.py
│   ├── core/
│   ├── output/
│   │   └── ip_map.html
│   ├── utils/
├── telnet_server/
│   ├── Server.java
│   ├── Makefile
│   ├── MANIFEST.MF
│   └── lib/
│       ├── exp4j-0.4.8.jar
│       └── gson-2.13.1.jar
├── LICENSE
├── README.md
└── requirements.txt
```

---

## Tools & Usage

### 1. Ethernet Frame Network Sniffer (`data_link/arp_ip_sniffer.py`)

Monitors your network and captures Ethernet frames (ARP or IP packets). Parses packets to determine sender/destination IP and MAC addresses. Detects potential ARP/IP spoofing or DDoS attacks by analyzing address mappings and packet frequency.

**MacOS/Linux**
```bash
cd tcp_ip_model
source .venv/bin/activate
pip install -r requirements.txt
sudo python3 data_link/arp_ip_sniffer.py
```

**Windows**
```cmd
cd tcp_ip_model
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
python data_link\arp_ip_sniffer.py
```

---

### 2. IP Geolocator (`ip_geolocator/main.py`)

Collects IP addresses from various sources (network sniffing, manual entry, or text files) and plots them on a map to visualize packet origins and destinations.

**Usage:**

```bash
cd tcp_ip_model
source .venv/bin/activate   # or use Windows activation above
pip install -r requirements.txt
python ip_geolocator/main.py [flags]
```

#### Flags

- `-n` : **Network sniffing** (default)  
  Obtain IP addresses by sniffing packets on your local network. Note that `sudo`/root permission is necessary for this setting.
  Example:  
  ```bash
  sudo python ip_geolocator/main.py -n
  ```

- `-t` : **Manual input**  
  Enter IP addresses manually when prompted.  
  Example:  
  ```bash
  python ip_geolocator/main.py -t
  ```

- `-d` : **Text file input**  
  Read IP addresses from a `.txt` file. You will be prompted for the file path.  
  Example:  
  ```bash
  python ip_geolocator/main.py -d
  ```

- `-m` : **Mapping mode** (default)  
  Display connections (arrows) between sender and destination IPs on the map.  
  Example:  
  ```bash
  python ip_geolocator/main.py -m
  ```

- `-l` : **Location-only mode**  
  Only display individual IP locations, without connections.  
  Example:  
  ```bash
  python ip_geolocator/main.py -l
  ```

#### Flag Combinations

- **Default:**  
  Network sniffing + mapping  
  ```bash
  sudo python ip_geolocator/main.py
  ```
- **Manual input + mapping:**  
  ```bash
  python ip_geolocator/main.py -t -m
  ```
- **Manual input + location-only:**  
  ```bash
  python ip_geolocator/main.py -t -l
  ```
- **Text file input + mapping:**  
  ```bash
  python ip_geolocator/main.py -d -m
  ```
- **Text file input + location-only:**  
  ```bash
  python ip_geolocator/main.py -d -l
  ```

**Notes:**
- You cannot use both `-n` and `-t`/`-d` at the same time.
- You cannot use both `-m` and `-l` at the same time.
- The output map will be saved in `ip_geolocator/output/ip_map.html`.

---

### 3. Telnet Server (`telnet_server/Server.java`)

A simple Telnet server implementation for experimenting with the TCP/IP stack at the application layer. Supports commands like `/echo`, `/math`, `/wiki`, and `/weather`.

**Build and Run (MacOS/Linux):**
```bash
cd tcp_ip_model/telnet_server
make        # Compiles and builds Server.jar
make run    # Runs the server
```
Or manually:
```bash
javac -cp "lib/exp4j-0.4.8.jar:lib/gson-2.13.1.jar" Server.java
jar cfm Server.jar MANIFEST.MF Server.class
java -jar Server.jar
```
Once the server is running, now, we can connect to it from another terminal as the client.

**Connect to the Server:**
```bash
telnet localhost 8080
```
- Type `exit` to disconnect.
- Supported commands:
  - `/echo <message>`: Echoes your message.
  - `/math <expression>`: Evaluates a math expression (supports constants π, e, φ and operators +, -, *, /, ^, %).
  - `/wiki <topic>`: Fetches a summary from Wikipedia via the `Wikipedia REST API`.
  - `/weather <location>`: Fetches weather info via `wttr.in`. Location format options: `City[ ,Country][ ,Region/State] | ZIP/Postal | Airport | Landmark`

---

## License

See [LICENSE](LICENSE) for details.

---

## Requirements

- Python 3.x (for Python tools)
- Java 11+ (for Telnet server)
- Python packages: see [requirements.txt](requirements.txt)
- Java libraries: exp4j, gson (included in `telnet_server/lib/`)

---

Thanks for checking it out 🤙
