import sys
import folium

def plot_ips_on_map(request_obj_lst, output_file="ip_map.html"):
    if not request_obj_lst:
        print("No IPs provided to map. Exiting...")
        sys.exit(1)
    
    ip_map = folium.Map(location=[0, 0], zoom_start=2)

    for ip_request in request_obj_lst:
        marker = folium.Marker(location=[ip_request.lat, ip_request.long],
            popup=f"{ip_request.ip_addr} - {ip_request.city}, {ip_request.country}",
            tooltip=ip_request.ip_addr)
        marker.addto(ip_map)

    ip_map.save(output_file)
    print(f"Map saved to {output_file}. Open it in your browser to view.")