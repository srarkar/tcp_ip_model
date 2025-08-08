import sys
import folium
from folium import Map, Marker, Icon, CustomIcon, Popup
import math
from branca.element import Template, MacroElement

from pathlib import Path
DEFAULT_SIZE = 30

# creates curved arc between 2 points (PolyLine modification)
def interpolate_arc(lat1, lon1, lat2, lon2, num_points=100, curvature=0.1):
    arc_points = []
    for i in range(num_points + 1):
        t = i / num_points
        # Linear interpolation
        lat = (1 - t) * lat1 + t * lat2
        lon = (1 - t) * lon1 + t * lon2
        # Add "curvature" perpendicular to line
        dx = lon2 - lon1
        dy = lat2 - lat1
        dist = math.sqrt(dx ** 2 + dy ** 2)
        offset = curvature * math.sin(math.pi * t) * dist

        # Rotate perpendicular vector
        nx = -dy
        ny = dx
        norm = math.sqrt(nx ** 2 + ny ** 2)
        if norm != 0:
            nx /= norm
            ny /= norm

        lat += ny * offset
        lon += nx * offset
        arc_points.append((lat, lon))
    return arc_points

# adds side panel with HTML + JS listener
def add_side_panel(ip_map):
    html = """
    {% macro html(this, kwargs) %}
    <style>
        #info-panel {
            position: absolute;
            top: 50px;
            right: 0;
            width: 300px;
            max-height: 80%;
            background-color: white;
            border: 1px solid #ccc;
            padding: 10px;
            overflow-y: auto;
            z-index: 9999;
            font-size: 14px;
        }
    </style>
    <div id="info-panel">
        <div id="marker-info"><b>Click on a marker to display information.</b></div>
    </div>
    <script>
        function updateInfoPanel(ip, city, region, country, zip) {
            let zipRow = "";
            if (zip && zip !== "000000") {
                zipRow = `<div><b>ZIP Code:</b> ${zip}</div>`;
            }
            document.getElementById('marker-info').innerHTML = `
                <div><b>IP:</b> ${ip}</div>
                <div><b>City:</b> ${city}</div>
                <div><b>Region:</b> ${region}</div>
                <div><b>Country:</b> ${country}</div>
                ${zipRow}
            `;
        }

        // Run after map loads
        document.addEventListener('DOMContentLoaded', function() {
            for (var key in window) {
                if (window[key] instanceof L.Marker) {
                    window[key].on('click', function(e) {
                        if (this.options.customData) {
                            let d = this.options.customData;
                            updateInfoPanel(d.ip, d.city, d.region, d.country, d.zip);
                        }
                    });
                }
            }
        });
    </script>
    {% endmacro %}
    """
    macro = MacroElement()
    macro._template = Template(html)
    ip_map.get_root().add_child(macro)




def get_icon_size(frequency, total):
    ratio = float(frequency + total) / total
    return (DEFAULT_SIZE * ratio, DEFAULT_SIZE * ratio)

def get_save_path(output_file):
    # Get the project root (parent of 'core')
    project_root = Path(__file__).resolve().parents[2]

    # Define the output path
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)  # Ensure the folder exists

    save_path = output_dir / output_file
    return save_path

marker_path = Path(__file__).resolve().parents[2] / "utils" / "images" / "map_marker.png"
if not marker_path.exists():
    print(f"Error: Marker image not found at {marker_path}")
    sys.exit(1)


def get_marker(ip_request, icon_size):
    icon = CustomIcon(
        icon_image=str(marker_path),
        icon_size=icon_size
    )
    marker = folium.Marker(
        location=[ip_request.lat, ip_request.long],
        icon=icon,
        tooltip=ip_request.ip_addr,
    )
    marker.options = marker.options or {}
    marker.options["customData"] = {
        "ip": ip_request.ip_addr,
        "city": ip_request.city,
        "region": ip_request.regionName,
        "country": ip_request.country,
        "zip": ip_request.zip
    }

    return marker
    

def plot_ips_on_map(request_obj_lst, frequency_map, ip_pairs, output_file = "ip_map.html"):
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
    add_side_panel(ip_map)
    ## TODO: take pairs of IP request objects as input
    ## call on plot connections to draw lines between them, using the lat and long of source and dest IP
    if len(ip_pairs) > 0:
        plot_connections(ip_map, ip_pairs)

    save_path = get_save_path(output_file)
    print(save_path)
    ip_map.save(save_path)
    print(f"Map saved to {save_path}. Open it in your browser to view.")

def plot_connections(map, ip_pairs):
    for pair in ip_pairs:
        src = pair[0]
        dest = pair[1]

        popup_content = f"From {src.city}, {src.country} to {dest.city}, {dest.country}"
        custom_popup = folium.Popup(
        popup_content,
        max_width=400,     # Maximum width in pixels
        min_width=250,     # Optional: minimum width
        max_height=250,    # Optional: height of the popup
        parse_html=True    # Optional: enables HTML parsing if your popup_content contains HTML
        )
        start = (src.lat, src.long)
        end = (dest.lat, dest.long)
        arc = interpolate_arc(*start, *end)

        folium.PolyLine(
        locations=arc,
        color='blue',
        weight=2,
        opacity=0.6,
        tooltip = f"{src.ip_addr} --> {dest.ip_addr}",
        popup = custom_popup
    ).add_to(map)