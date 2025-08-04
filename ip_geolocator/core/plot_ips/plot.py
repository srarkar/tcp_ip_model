import sys
import folium

from pathlib import Path

## TODO: add connections between sender and destination if settings[mapping] is True

# print(f"Map saved to {save_path}")
def get_icon_size(frequency, total):
    ratio = float(frequency + total) / total
    return (28 * ratio, 28 * ratio)

def get_save_path(output_file):
    # Get the project root (parent of 'core')
    project_root = Path(__file__).resolve().parents[2]

    # Define the output path
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)  # Ensure the folder exists

    save_path = output_dir / output_file
    return save_path

def get_marker(ip_request, icon_size):
    return folium.Marker(icon=folium.Icon(icon="info-sign", icon_size=icon_size), location=[ip_request.lat, ip_request.long],
            popup=f"{ip_request.ip_addr} - {ip_request.city}, {ip_request.country}",
            tooltip=ip_request.ip_addr)
    

def plot_ips_on_map(request_obj_lst, frequency_map, output_file = "ip_map.html"):
    if not request_obj_lst:
        print("No IPs provided to map. Exiting...")
        sys.exit(1)
    
    ip_map = folium.Map(location=[0, 0], zoom_start=2)
    total_ips = sum(frequency_map.values())

    for ip_request in request_obj_lst:
        frequency = frequency_map[ip_request.ip_addr]
        icon_size = get_icon_size(frequency, total_ips)
        marker = get_marker(ip_request, icon_size)
        marker.add_to(ip_map)

    ## TODO: take pairs of IP request objects as input
    ## call on plot connectiosn to draw lines between them, using the lat and long of source and dest IP


    save_path = get_save_path(output_file)
    print(save_path)
    ip_map.save(save_path)
    print(f"Map saved to {save_path}. Open it in your browser to view.")

def plot_connections(ip_pairs)