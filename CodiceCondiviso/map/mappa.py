import folium
from sklearn.cluster import DBSCAN
import numpy as np
from haversine import haversine, Unit
from sklearn.metrics.pairwise import pairwise_distances

"""

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
"""



import folium
from sklearn.cluster import DBSCAN
import numpy as np
from haversine import haversine
from sklearn.metrics.pairwise import pairwise_distances
import re

# Funzione per leggere il file e parsare le informazioni
def read_file(file_path):
    places = []
    coordinates = []
    images = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Usa una regex per estrarre i campi
            match = re.match(r"^(.*?), \(([^)]+)\), \(([^)]+)\)", line.strip())
            if match:
                place = match.group(1).strip()
                coord = tuple(map(float, match.group(2).split(", ")))
                image_urls = match.group(3).split(", ")
                places.append(place)
                coordinates.append(coord)
                images.append(image_urls)
    
    return places, np.array(coordinates), images


# File di input
file_path = "map/infos.txt"  # Cambia con il tuo percorso
places, coords, images = read_file(file_path)

# Funzione per calcolare la matrice delle distanze haversine
def haversine_distance_matrix(coordinates):
    return pairwise_distances(coordinates, metric=lambda x, y: haversine(x, y))

# Calcola la matrice delle distanze in chilometri
distance_matrix = haversine_distance_matrix(coords)

# Applica il clustering DBSCAN
eps_distance = 350  # Cambia la soglia di distanza (in km)
dbscan = DBSCAN(eps=eps_distance, min_samples=1, metric="precomputed")
cluster_labels = dbscan.fit_predict(distance_matrix)

# Crea la mappa centrata sul primo punto
m = folium.Map(location=coords[0].tolist(), zoom_start=6)

# Definisci 10 colori per i cluster
cluster_colors = [
    "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF",
    "#800000", "#008000", "#000080", "#808000"
]

# Usa questi colori ciclicamente per i cluster
for i, (lat, lon) in enumerate(coords):
    label = cluster_labels[i]
    color = cluster_colors[label % len(cluster_colors)] if label != -1 else "#000000"  # Nero per il rumore



# Aggiungi i marker sulla mappa e le linee tra i punti dello stesso cluster
for label in set(cluster_labels):
    # Trova i punti che appartengono a questo cluster
    cluster_coords = [coords[i] for i in range(len(coords)) if cluster_labels[i] == label]
    
    # Aggiungi le linee tra i punti dello stesso cluster
    if len(cluster_coords) > 1:
        folium.PolyLine(cluster_coords, color=cluster_colors[label], weight=2.5, opacity=1).add_to(m)

    # Aggiungi i marker sulla mappa
    for i, (lat, lon) in enumerate(coords):
        label = cluster_labels[i]
        color = cluster_colors[label] if label != -1 else "#000000"  # Nero per il rumore

        # ID univoco per il carosello
        carousel_id = f"carousel_{i}"
        
        # Impostiamo la prima immagine come visibile, le altre nascoste
        image_html = "".join([
            f'<img class="carousel-item-{i}" src="{url}" style="display:none; width:150px;height:auto;">'
            for url in images[i]
        ])
        
        # Imposta la prima immagine come visibile
        image_html = image_html.replace('style="display:none"', 'style="display:block"', 1)

        html_content = f'''
            <div style="text-align:center; width:150px;height:150px;">
                <h4>{places[i]}</h4>
                <div id="{carousel_id}" class="carousel">
                    {image_html}
                    <button class="prev" onclick="prevImage('{carousel_id}')">&#10094;</button>
                    <button class="next" onclick="nextImage('{carousel_id}')">&#10095;</button>
                </div>
            </div>
        '''
        popup = folium.Popup(html_content, max_width=300)

        # Aggiungi il marker con popup
        folium.CircleMarker(
            location=(lat, lon),
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            popup=popup
        ).add_to(m)

# Salva la mappa in un file HTML
map_filename = f"map/map_{eps_distance}km.html"
m.save(map_filename)

# Aggiungi il JavaScript al file HTML generato
with open(map_filename, "r", encoding="utf-8") as file:
    html_content = file.read()

# Script JavaScript per i caroselli
carousel_script = '''
<script>
    function showImage(carouselId, index) {
        const carousel = document.getElementById(carouselId);
        const items = carousel.querySelectorAll('img');
        items.forEach((item, i) => {
            item.style.display = i === index ? 'block' : 'none';
        });
    }
    function prevImage(carouselId) {
        const carousel = document.getElementById(carouselId);
        const items = carousel.querySelectorAll('img');
        const currentIndex = Array.from(items).findIndex(item => item.style.display === 'block');
        const newIndex = (currentIndex - 1 + items.length) % items.length;
        showImage(carouselId, newIndex);
    }
    function nextImage(carouselId) {
        const carousel = document.getElementById(carouselId);
        const items = carousel.querySelectorAll('img');
        const currentIndex = Array.from(items).findIndex(item => item.style.display === 'block');
        const newIndex = (currentIndex + 1) % items.length;
        showImage(carouselId, newIndex);
    }
    document.addEventListener("DOMContentLoaded", function() {
        document.querySelectorAll('.carousel').forEach(carousel => {
            const carouselId = carousel.id;
            showImage(carouselId, 0); // Mostra la prima immagine all'inizio
        });
    });
</script>
'''

# Aggiungi lo script al file HTML
html_content = html_content.replace("</body>", f"{carousel_script}</body>")
with open(map_filename, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"Map saved as {map_filename}")
