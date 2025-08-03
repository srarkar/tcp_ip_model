import sys
import folium

from pathlib import Path

# print(f"Map saved to {save_path}")
def get_save_path(output_file):
    # Get the project root (parent of 'core')
    project_root = Path(__file__).resolve().parents[2]

    # Define the output path
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)  # Ensure the folder exists

    save_path = output_dir / output_file
    return save_path

def plot_ips_on_map(request_obj_lst, output_file = "ip_map.html"):
    if not request_obj_lst:
        print("No IPs provided to map. Exiting...")
        sys.exit(1)
    
    ip_map = folium.Map(location=[0, 0], zoom_start=2)

    for ip_request in request_obj_lst:
        marker = folium.Marker(location=[ip_request.lat, ip_request.long],
            popup=f"{ip_request.ip_addr} - {ip_request.city}, {ip_request.country}",
            tooltip=ip_request.ip_addr)
        marker.add_to(ip_map)


    save_path = get_save_path(output_file)
    print(save_path)
    ip_map.save(save_path)
    print(f"Map saved to {save_path}. Open it in your browser to view.")