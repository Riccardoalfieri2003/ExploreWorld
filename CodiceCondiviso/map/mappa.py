import folium
from sklearn.cluster import DBSCAN
import numpy as np
from haversine import haversine, Unit
from sklearn.metrics.pairwise import pairwise_distances


# Choose a distance threshold (in kilometers)
eps_distance = 200  # Change this value to set the clustering distance threshold

# Example list of coordinates from Instagram posts
coordinates = [
    (48.858844, 2.294351),  # Eiffel Tower
    (48.858093, 2.294694),  # Nearby point
    (40.689247, -74.044502),  # Statue of Liberty
    (40.689450, -74.045200),  # Nearby point
    (51.500729, -0.124625),  # Big Ben
    (51.7504622, -1.2887872),  # Oxford
    (40.9623301,14.5379536) #Cicciano
]

# Convert to a NumPy array
coords = np.array(coordinates)

# Define a function to compute haversine distances in km
def haversine_distance_matrix(coordinates):
    return pairwise_distances(coordinates, metric=lambda x, y: haversine(x, y))

# Calculate the distance matrix in kilometers
distance_matrix = haversine_distance_matrix(coords)

# Apply DBSCAN clustering
dbscan = DBSCAN(eps=eps_distance, min_samples=1, metric="precomputed")  # eps in km
cluster_labels = dbscan.fit_predict(distance_matrix)

# Create a map centered at the first point
m = folium.Map(location=coords[0].tolist(), zoom_start=3)

# Define colors for clusters
cluster_colors = [
    "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"
]
cluster_colors += ["#" + ''.join(np.random.choice(list("0123456789ABCDEF"), 6)) for _ in range(100)]

for i, (lat, lon) in enumerate(coords):
    label = cluster_labels[i]
    color = cluster_colors[label] if label != -1 else "#000000"  # Black for noise

    # Custom HTML content for the popup
    html_content = f'''
        <div style="text-align:center;">
            <h4>Luogo: {label if label != -1 else "Noise"}</h4>
            <img src="https://via.placeholder.com/100" alt="Sample Image" style="width:150px;height:auto;">
            <p><a href="https://example.com" target="_blank">More Info</a></p>
        </div>
    '''
    popup = folium.Popup(html_content, max_width=300)

    # Adding the marker with a popup
    folium.CircleMarker(
        location=(lat, lon),
        radius=5,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        popup=popup
    ).add_to(m)

# Optionally connect points in the same cluster
for label in set(cluster_labels):
    if label == -1:  # Skip noise
        continue
    cluster_points = coords[cluster_labels == label]
    for i in range(len(cluster_points) - 1):
        folium.PolyLine(
            locations=[cluster_points[i].tolist(), cluster_points[i + 1].tolist()],
            color=cluster_colors[label],
            weight=2
        ).add_to(m)

# Save map to HTML file
map_filename = f"map_with_clusters_{eps_distance}km.html"
m.save(map_filename)
print(f"Map saved as {map_filename}")