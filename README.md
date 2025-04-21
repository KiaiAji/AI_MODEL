# 🗺️ SHORTEST PATH WITH GENETIC ALGORITHM Kampus UNIB
## Proyek ini akan menampilkan rute terpendek antar lokasi di lingkungan Kampus Universitas Bengkulu menggunakan algoritma Genetika

<h2>Analisis kesalahan/kekurangan dari AI yang dibuat</h2>
📌Algoritma genetika memiliki sejumlah keunggulan penting dalam menangani masalah optimasi yang rumit. Kemampuannya untuk secara efisien menjelajahi ruang solusi yang luas, menghindari jebakan optimum lokal melalui mekanisme mutasi, serta fleksibilitasnya dalam berbagai jenis permasalahan menjadikannya pilihan yang menarik. Selain itu, sifat adaptif dan kemudahan dalam melakukan paralelisasi memberikan keuntungan dalam hal komputasi. Namun, algoritma ini juga memiliki beberapa kelemahan yang perlu diperhatikan. Proses konvergensi yang kadang-kadang lambat, kesulitan dalam menentukan parameter yang paling sesuai, tantangan dalam merancang representasi solusi yang efektif, serta tidak adanya jaminan untuk menemukan solusi global yang optimal merupakan batasan yang harus diperhatikan dalam penerapannya. Hal ini juga dirasakan oleh kelompok kami, di mana terdapat beberapa aspek yang sulit dilaksanakan akibat kompleksitas algoritma ini.


📌Berikut hasil pengamatan kami:
1. Rute yang diberikan belum sesuai dengan google maps, jalan yang seharusnya satu arah yang dimana mengharuskan user untuk putar arah dan mencari jalan tercepat tidak ditampilkan.
3. Loading untuk menjalankan kode yang telah dibuat masih tergolong lambat
![alt text](https://github.com/KiaiAji/AI_MODEL/blob/main/Cuplikan%20layar%202025-04-21%20231555.png?raw=true)
5. tidak bisa melihat salah satu jalur( motor saja, atau jalan kaki saja , atau mobilsaja)

📌Masalah yang kami temukan no 1 dan 3 yaitu jalan antar gedung yang tidak dapat di akses dengan satu arah sesuai dengan peraturan Jalan Universitas Bengkulu akan menyebabkan beberapa komplikasi pada sistem kami yaitu sistem makin lambat, serta rentan akan eror, hal ini juga berlaku untuk  tidak bisa melihat salah satu jalur. 

📌Yang paling berdampak dari algoritma ini adalah bagian loading saat memuat inputan yang di inginkan, dalam proses ini user tidak dapat memasukan tempat yang tidak sesuai dengan yang ada pada inputan peta. misalkan, dekanat dan Dekanat. input dekanat (dengan huruf d kecil), tidak akan ter baca oleh sistem karena yang ada pada maps adalah Dekanat (menggunakan D Kapital). karena menginputtkan darta dari banyaknya fungsi ini akan menjadi salah satu dari banyak faktor mengapa proses memuat data apada program kami lambat.

# Penjelasan Kode Pencari Rute Universitas Bengkulu

Menjelaskan setiap bagian dari kode Python dengan mengunakan algoritma (Genetic Algrithm) untuk aplikasi pencari rute di sekitar Universitas Bengkulu.


**Proyek: Sistem Navigasi Kampus UNIB dengan Algoritma Genetic Algrithm**
---

## 1. Import Library
📄 **Kode:**
```python
# === IMPORT LIBRARY ===
from math import radians, cos, sin, sqrt, atan2   # Untuk menghitung jarak antara dua titik di bumi
import osmnx as ox                                 # Untuk mengambil dan memproses jaringan jalan dari OpenStreetMap
from geopy.geocoders import Nominatim              # Untuk mengubah nama lokasi jadi koordinat
import networkx as nx                               # Untuk representasi graf dan perhitungan rute
import random                                     # Untuk proses acak pada algoritma genetika
import folium                                     # Untuk menampilkan peta interaktif
```

Kode mengimpor library-library berikut:

* `math`: Digunakan untuk perhitungan matematika, khususnya fungsi trigonometri untuk menghitung jarak antar koordinat (`radians`, `cos`, `sin`, `sqrt`, `atan2`).
* `osmnx`: Library Python untuk mengunduh, memodelkan, menganalisis, dan memvisualisasikan jaringan jalan dari OpenStreetMap. Digunakan di sini untuk mendapatkan graf jalan di area Universitas Bengkulu.
* `geopy.geocoders.Nominatim`: Modul dari library `geopy` yang digunakan untuk melakukan geocoding, yaitu mengubah nama lokasi menjadi koordinat lintang dan bujur.
* `networkx`: Library Python untuk membuat, memanipulasi, dan mempelajari struktur, dinamika, dan fungsi dari graf kompleks. Digunakan di sini untuk merepresentasikan jaringan jalan dan melakukan perhitungan rute Dijkstra (sebagai pembanding dan inisialisasi populasi algoritma genetika).
* `random`: Modul Python untuk menghasilkan bilangan acak. Digunakan dalam implementasi algoritma genetika untuk inisialisasi populasi, crossover, dan mutasi.
* `folium`: Library Python yang memungkinkan pembuatan peta interaktif berbasis Leaflet. Digunakan untuk menampilkan rute terbaik di atas peta OpenStreetMap.

## 2. Fungsi `calculate_great_circle_distance(lat1, lon1, lat2, lon2)`
📄 **Kode:**
```python
# === FUNGSI UNTUK MENGHITUNG JARAK ===
def calculate_great_circle_distance(lat1, lon1, lat2, lon2):
    """
    Menghitung jarak lintasan melengkung (great-circle distance)
    antara dua titik lintang dan bujur.
    """
    R = 6371000   # Radius bumi dalam meter
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)
    a = sin(delta_phi / 2)**2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c
```

* Fungsi ini menghitung jarak antara dua titik di permukaan bumi berdasarkan koordinat lintang dan bujur menggunakan formula *great-circle distance* (jarak lintasan melengkung).
* Formula ini memperhitungkan kelengkungan bumi untuk memberikan perkiraan jarak yang lebih akurat dibandingkan dengan perhitungan jarak Euclidean sederhana.
* `R = 6371000`: Radius bumi dalam meter.
* Fungsi ini menerima input berupa lintang dan bujur dari dua titik dan mengembalikan jarak antara keduanya dalam meter.

## 3. Fungsi `shortest_path_genetic(...)`
📄 **Kode:**
```python
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
            for _ in range(20):   # Batas maksimum langkah
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
                return float('inf')   # Jika edge tidak ada
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
```
* Fungsi ini mengimplementasikan algoritma genetika untuk mencari rute terpendek antara titik awal (`start`) dan titik akhir (`end`) dalam graf jalan (`G`).
* **`edge_lengths`:** Dictionary untuk menyimpan panjang setiap edge dalam graf. Jika panjang tidak tersedia dalam data edge, jarak *great-circle* dihitung.
* **`fitness_cache`:** Dictionary untuk menyimpan nilai fitness dari setiap rute yang telah dihitung, untuk menghindari perhitungan berulang.
* **`initialize_population()`:**
    * Membuat populasi awal dari calon rute.
    * Mencoba menambahkan rute terpendek yang ditemukan oleh algoritma Dijkstra (jika memungkinkan) sebagai salah satu individu dalam populasi awal.
    * Menghasilkan rute acak dengan batasan jumlah langkah untuk mengisi sisa populasi.
    * Menambahkan rute langsung dari titik awal ke titik akhir sebagai bagian dari populasi awal.
* **`calculate_path_length(path)`:** Menghitung total panjang (jarak) dari sebuah rute dengan menjumlahkan panjang setiap edge yang dilalui. Jika ada edge yang tidak ditemukan, fungsi mengembalikan nilai tak hingga (`float('inf')`).
* **`fitness_function(path)`:** Menghitung nilai fitness suatu rute. Semakin pendek rute, semakin tinggi nilai fitnessnya (menggunakan invers dari panjang rute).
* **`crossover(parent1, parent2)`:** Menggabungkan dua rute induk (`parent1`, `parent2`) untuk menghasilkan rute anak baru. Proses crossover dilakukan dengan mencari node yang sama di kedua induk dan menggabungkan sebagian dari kedua rute tersebut.
* **`mutate(path)`:** Melakukan mutasi pada suatu rute dengan mengganti salah satu node tengah secara acak dengan node tetangga dari node sebelumnya yang terhubung ke node setelahnya.
* **Proses Evolusi:**
    * Mengulang sebanyak `generations`.
    * Menghitung nilai fitness untuk setiap rute dalam populasi.
    * Memilih induk berdasarkan nilai fitness (roulette wheel selection sederhana dengan mengambil dua kandidat acak dan memilih yang terbaik).
    * Menciptakan populasi baru dengan melakukan crossover antara induk dan kemudian memutasinya.
    * Memperbarui populasi untuk generasi berikutnya.
* Fungsi ini mengembalikan rute terbaik yang ditemukan dan panjang rute tersebut.

## 4. Fungsi `calculate_travel_times(jarak)`
📄 **Kode:**
```python
# === FUNGSI UNTUK MENGHITUNG WAKTU PERJALANAN ===
def calculate_travel_times(jarak):
    """
    Mengubah jarak menjadi estimasi waktu perjalanan berdasarkan moda transportasi.
    """
    speeds = {
        'jalan_kaki': 1.11,   # 4 km/jam
        'motor': 16.67,      # 60 km/jam
        'mobil': 11.11        # 40 km/jam
    }
    times = {}
    for mode, speed in speeds.items():
        seconds = jarak / speed
        mins, secs = divmod(int(seconds), 60)
        times[mode] = f"{mins:02d} menit {secs:02d} detik" if secs > 0 else f"{mins:02d} menit"
    return times
```

* Fungsi ini memperkirakan waktu perjalanan berdasarkan jarak (`jarak` dalam meter) untuk tiga moda transportasi: jalan kaki, motor, dan mobil.
* Kecepatan rata-rata untuk setiap moda didefinisikan dalam dictionary `speeds` (dalam meter per detik).
* Fungsi ini menghitung waktu dalam detik, kemudian mengonversinya menjadi menit dan detik, dan mengembalikan dictionary yang berisi perkiraan waktu tempuh untuk setiap moda.

## 5. Fungsi `main()`
📄 **Kode:**
```python
# === PROGRAM UTAMA ===
def main():
    try:
        # Mengambil graf jalan di Universitas Bengkulu
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

    # Menemukan node terdekat dari graf jalan
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

    # Membuat peta interaktif
    m = folium.Map(location=start_coords, zoom_start=16, tiles='OpenStreetMap')

    # Menambahkan rute
    route_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route]
    folium.PolyLine(route_coords, color='#FF0000', weight=6, opacity=0.7).add_to(m)

    # Menambahkan marker lokasi
    folium.CircleMarker(location=start_coords, radius=8, color='#0F9D58', fill=True, fill_color='#0F9D58').add_to(m)
    folium.CircleMarker(location=end_coords, radius=8, color='#4285F4', fill=True, fill_color='#4285F4').add_to(m)

    # Menghitung estimasi waktu
    waktu_perjalanan = calculate_travel_times(jarak)
    jarak_km = jarak / 1000
    jarak_text = f"{jarak_km:.1f} km".replace('.', ',')

    # Menambahkan box info ke peta (HTML custom)
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
            <div style="text-align: center; width: 33%;">
                <div>Jalan Kaki</div>
                <div>{waktu_perjalanan['jalan_kaki']}</div>
            </div>
            <div style="text-align: center; width: 33%;">
                <div>Motor</div>
                <div>{waktu_perjalanan['motor']}</div>
            </div>
            <div style="text-align: center; width: 33%;">
                <div>Mobil</div>
                <div>{waktu_perjalanan['mobil']}</div>
            </div>
        </div>
    </div>
    """

    m.get_root().html.add_child(folium.Element(top_html))
    m.get_root().html.add_child(folium.Element(bottom_html))

    # Menyimpan peta
    file_name = "map_unib.html"
    m.save(file_name)
    print(f"\nBuka file '{file_name}' di live server browser")
```
* Ini adalah fungsi utama yang menjalankan program.
* **Mengambil Graf Jalan:** Menggunakan `ox.graph_from_place()` untuk mengunduh dan membuat graf jalan dari area "Universitas Bengkulu, Indonesia" dari OpenStreetMap. Graf disederhanakan dan diubah menjadi tidak berarah.
* **Inisialisasi Geocoder:** Membuat instance dari `Nominatim` untuk mengubah nama lokasi menjadi koordinat.
* **Input Lokasi:** Meminta pengguna untuk memasukkan lokasi awal dan tujuan.
* **`get_coords(place)`:** Fungsi lokal untuk mengubah nama lokasi menjadi koordinat lintang dan bujur menggunakan geocoder.
* **Mendapatkan Koordinat Awal dan Tujuan:** Menggunakan `get_coords()` untuk mendapatkan koordinat dari lokasi awal dan tujuan yang dimasukkan pengguna.
* **Mencari Node Terdekat:** Menggunakan `ox.distance.nearest_nodes()` untuk menemukan node terdekat dalam graf jalan (`G`) dengan koordinat awal dan tujuan.
* **Mencari Rute Terpendek:** Memanggil fungsi `shortest_path_genetic()` untuk menemukan rute terpendek antara node awal dan akhir.
* **Membuat Peta Interaktif:** Membuat objek peta `folium.Map()` yang berpusat di lokasi awal.
* **Menambahkan Rute ke Peta:** Mengambil koordinat dari setiap node dalam rute terbaik dan menampilkannya sebagai garis (`folium.PolyLine`) di peta.
* **Menambahkan Marker Lokasi:** Menambahkan marker (`folium.CircleMarker`) untuk menandai lokasi awal dan tujuan di peta.
* **Menghitung dan Menampilkan Waktu Perjalanan:** Memanggil `calculate_travel_times()` untuk mendapatkan perkiraan waktu perjalanan berdasarkan jarak rute terbaik. Jarak juga ditampilkan dalam kilometer.
* **Menambahkan Informasi ke Peta (HTML Custom):** Membuat elemen HTML untuk menampilkan informasi lokasi awal, lokasi tujuan, jarak, dan perkiraan waktu perjalanan untuk setiap moda transportasi di bagian atas dan bawah peta. Informasi ini ditampilkan dalam kotak yang tetap di layar.
* **Menyimpan Peta:** Menyimpan peta interaktif ke dalam file HTML (`map_unib.html`).
* **Memberikan Instruksi:** Mencetak instruksi kepada pengguna untuk membuka file HTML di browser dengan *live server* agar peta interaktif dapat dilihat dengan benar.

## 6. Eksekusi Program
📄 **Kode:**
```python
# === EKSEKUSI PROGRAM ===
if __name__ == "__main__":
    main()
```
* Bagian `if __name__ == "__main__":` memastikan bahwa fungsi `main()` hanya dijalankan ketika skrip dieksekusi secara langsung (bukan ketika diimpor sebagai modul).
