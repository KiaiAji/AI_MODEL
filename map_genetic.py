# === IMPORT LIBRARY ===
from math import radians, cos, sin, sqrt, atan2  # Untuk menghitung jarak antara dua titik di bumi
import osmnx as ox                      # Untuk mengambil dan memproses jaringan jalan dari OpenStreetMap
from geopy.geocoders import Nominatim # Untuk mengubah nama lokasi jadi koordinat
import networkx as nx                  # Untuk representasi graf dan perhitungan rute
import random                          # Untuk proses acak pada algoritma genetika
import folium                          # Untuk menampilkan peta interaktif


# === FUNGSI UNTUK MENGHITUNG JARAK ===
def calculate_great_circle_distance(lat1, lon1, lat2, lon2):
    """
    Menghitung jarak lintasan melengkung (great-circle distance)
    antara dua titik lintang dan bujur.
    """
    R = 6371000  # Radius bumi dalam meter
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)
    a = sin(delta_phi / 2)**2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


# === ALGORITMA GENETIKA UNTUK MENENTUKAN RUTE TERPENDEK ===
def shortest_path_genetic(G, start, end, population_size=10, generations=30, mutation_rate=0.2):
    """
    Menemukan rute terbaik menggunakan pendekatan algoritma genetika.
    """
    # Simpan panjang edge
    edge_lengths = {}
    for u, v, data in G.edges(data=True):
        edge_lengths[(u, v)] = data.get('length',
            calculate_great_circle_distance(
                G.nodes[u]['y'], G.nodes[u]['x'],
                G.nodes[v]['y'], G.nodes[v]['x']
            ))

    fitness_cache = {}

    def initialize_population():
        """
        Membuat populasi awal dari rute acak dan hasil dijkstra.
        """
        population = []
        try:
            dijkstra_path = nx.shortest_path(G, start, end, weight='length')
            population.append(dijkstra_path)
        except:
            pass

        def generate_random_path():
            path = [start]
            current = start
            visited = set([start])
            for _ in range(20):  # Batas maksimum langkah
                if current == end:
                    return path
                neighbors = [n for n in G.neighbors(current) if n not in visited]
                if not neighbors:
                    break
                next_node = random.choice(neighbors)
                path.append(next_node)
                visited.add(next_node)
                current = next_node
            return None

        while len(population) < population_size:
            path = generate_random_path()
            if path and path not in population:
                population.append(path)

        while len(population) < population_size:
            population.append([start, end])
        return population

    def calculate_path_length(path):
        """
        Menghitung panjang total suatu rute.
        """
        length = 0
        for u, v in zip(path[:-1], path[1:]):
            if (u, v) in edge_lengths:
                length += edge_lengths[(u, v)]
            elif (v, u) in edge_lengths:
                length += edge_lengths[(v, u)]
            else:
                return float('inf')  # Jika edge tidak ada
        return length

    def fitness_function(path):
        """
        Menghitung fitness (semakin kecil jarak, semakin besar fitness).
        """
        path_tuple = tuple(path)
        if path_tuple in fitness_cache:
            return fitness_cache[path_tuple]
        length = calculate_path_length(path)
        fitness = 1/length if length != float('inf') else 0
        fitness_cache[path_tuple] = fitness
        return fitness

    def crossover(parent1, parent2):
        """
        Menggabungkan dua parent untuk menghasilkan anak baru.
        """
        common_nodes = set(parent1[1:-1]) & set(parent2[1:-1])
        if not common_nodes:
            return parent1 if random.random() < 0.5 else parent2
        crossover_point = random.choice(list(common_nodes))
        idx1 = parent1.index(crossover_point)
        idx2 = parent2.index(crossover_point)
        new_path = parent1[:idx1] + parent2[idx2:]
        seen = set()
        unique_path = []
        for node in new_path:
            if node not in seen:
                unique_path.append(node)
                seen.add(node)
        return unique_path

    def mutate(path):
        """
        Mutasi jalur dengan mengganti salah satu node tengah secara acak.
        """
        if random.random() < mutation_rate and len(path) > 2:
            mutate_pos = random.randint(1, len(path)-2)
            prev_node = path[mutate_pos-1]
            next_node = path[mutate_pos+1] if mutate_pos+1 < len(path) else end
            candidates = []
            for neighbor in G.neighbors(prev_node):
                if (neighbor, next_node) in edge_lengths or (next_node, neighbor) in edge_lengths:
                    candidates.append(neighbor)
            if candidates:
                path[mutate_pos] = random.choice(candidates)
        return path

    # Jalankan proses evolusi
    population = initialize_population()
    for generation in range(generations):
        fitness_values = [fitness_function(p) for p in population]
        parents = []
        for _ in range(population_size):
            candidates = random.sample(list(zip(population, fitness_values)), k=2)
            parents.append(max(candidates, key=lambda x: x[1])[0])

        new_population = []
        for i in range(0, len(parents), 2):
            if i+1 >= len(parents):
                new_population.append(parents[i])
                continue
            parent1, parent2 = parents[i], parents[i+1]
            child1 = mutate(crossover(parent1, parent2))
            child2 = mutate(crossover(parent2, parent1))
            new_population.extend([child1, child2])

        population = new_population

    best_path = max(population, key=lambda p: fitness_function(p))
    best_length = calculate_path_length(best_path)
    return best_path, best_length


# === FUNGSI UNTUK MENGHITUNG WAKTU PERJALANAN ===
def calculate_travel_times(jarak):
    """
    Mengubah jarak menjadi estimasi waktu perjalanan berdasarkan moda transportasi.
    """
    speeds = {
        'jalan_kaki': 1.11,  # 4 km/jam
        'motor': 16.67,      # 60 km/jam
        'mobil': 11.11       # 40 km/jam
    }
    times = {}
    for mode, speed in speeds.items():
        seconds = jarak / speed
        mins, secs = divmod(int(seconds), 60)
        times[mode] = f"{mins:02d} menit {secs:02d} detik" if secs > 0 else f"{mins:02d} menit"
    return times


# === PROGRAM UTAMA ===
def main():
    try:
        # Ambil graf jalan di Universitas Bengkulu
        G = ox.graph_from_place("Universitas Bengkulu, Indonesia", network_type='all', simplify=True)
        G = G.to_undirected()
    except Exception as e:
        print(f"Error: {e}")
        return

    # Inisialisasi geocoder
    geolocator = Nominatim(user_agent="map_unib")

    # Input dari user
    start_loc = input("Masukkan lokasi awal: ").strip()
    end_loc = input("Masukkan lokasi tujuan: ").strip()

    def get_coords(place):
        """
        Mengubah nama lokasi menjadi koordinat.
        """
        try:
            location = geolocator.geocode(place + ", Bengkulu, Indonesia")
            if location:
                return (location.latitude, location.longitude)
            return None
        except:
            return None

    start_coords = get_coords(start_loc)
    end_coords = get_coords(end_loc)

    if not start_coords or not end_coords:
        print("Tidak dapat melanjutkan karena lokasi tidak valid!")
        return

    # Temukan node terdekat dari graf jalan
    start_node = ox.distance.nearest_nodes(G, start_coords[1], start_coords[0])
    end_node = ox.distance.nearest_nodes(G, end_coords[1], end_coords[0])

    print("\nMencari rute")
    try:
        route, jarak = shortest_path_genetic(G, start_node, end_node)
        if not route or jarak == 0:
            print("Error dalam mencari rute!")
            return
        print(f"Jarak rute terbaik: {jarak:.2f} meter")
    except Exception as e:
        print(f"Error dalam menghitung rute: {e}")
        return

    # Buat peta interaktif
    m = folium.Map(location=start_coords, zoom_start=16, tiles='OpenStreetMap')

    # Tambahkan rute
    route_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route]
    folium.PolyLine(route_coords, color='#FF0000', weight=6, opacity=0.7).add_to(m)

    # Tambahkan marker lokasi
    folium.CircleMarker(location=start_coords, radius=8, color='#0F9D58', fill=True, fill_color='#0F9D58').add_to(m)
    folium.CircleMarker(location=end_coords, radius=8, color='#4285F4', fill=True, fill_color='#4285F4').add_to(m)

    # Hitung estimasi waktu
    waktu_perjalanan = calculate_travel_times(jarak)
    jarak_km = jarak / 1000
    jarak_text = f"{jarak_km:.1f} km".replace('.', ',')

    # Tambahkan box info ke peta (HTML custom)
    # HTML untuk box atas
    top_html = f"""
    <div style="position: fixed; top: 20px; left: 20px; right: 20px;
                background: white; padding: 15px;
                border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                z-index: 9999; font-family: 'Segoe UI', Arial, sans-serif;">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="width: 8px; height: 8px; background: #0F9D58; border-radius: 50%; margin-right: 10px;"></div>
            <div style="flex-grow: 1;">
                <div style="font-size: 16px; color: #666;">Lokasi Awal</div>
                <div style="font-size: 20px; font-weight: bold;">{start_loc}</div>
            </div>
            <div style="font-size: 20px; color: #4285F4; white-space: nowrap;">
                {jarak_text}
            </div>
        </div>
        
        <div style="display: flex; align-items: center;">
            <div style="width: 8px; height: 8px; background: #4285F4; border-radius: 50%; margin-right: 10px;"></div>
            <div style="flex-grow: 1;">
                <div style="font-size: 16px; color: #666;">Lokasi Tujuan</div>
                <div style="font-size: 20px; font-weight: bold;">{end_loc}</div>
            </div>
        </div>
    </div>
    """

    # HTML untuk box bawah
    bottom_html = f"""
    <div style="position: fixed; bottom: 20px; left: 20px; right: 20px;
                background: white; padding: 15px;
                border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                z-index: 9999; font-family: 'Segoe UI', Arial, sans-serif;">
        
        <div style="display: flex; justify-content: space-between; font-size: 16px;">
            <div style="text-align: center; width: 50%;">
                <div>Jalan Kaki</div>
                <div>{waktu_perjalanan['jalan_kaki']}</div>
            </div>
            <div style="text-align: center; width: 50%;">
                <div>Motor</div>
                <div>{waktu_perjalanan['motor']}</div>
            </div>
            <div style="text-align: center; width: 50%;">
                <div>Mobil</div>
                <div>{waktu_perjalanan['mobil']}</div>
            </div>
        </div>
    </div>
    """
    
    m.get_root().html.add_child(folium.Element(top_html))
    m.get_root().html.add_child(folium.Element(bottom_html))

    # === PERBARUI FILE HTML ===
    file_name = "map_unib.html"
    m.save(file_name)
    print(f"\nBuka file '{file_name}' di live server browser")


# === EKSEKUSI PROGRAM ===
if __name__ == "__main__":
    main()
