import folium

def create_map(filepath, lat, lon, zoom=10):
    # Center the map at the given coords
    my_map = folium.Map(location=[lat, lon], zoom_start=zoom)

    # Drop a pin
    folium.Marker(location=[lat, lon], popup="Guessed Location").add_to(my_map)

    # Save to an HTML file
    my_map.save(filepath)
    print(f"Interactive map saved to {filepath}")
