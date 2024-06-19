import requests
import folium
import geopandas as gpd
import pandas as pd
from geopy.geocoders import Nominatim
import urllib.request
import openrouteservice
from openrouteservice import convert
import openrouteservice as ors
import ast
import json
import os
import fiona
import glob


try:
    urllib.request.urlopen('http://google.com')
    pass
except:
    print("TIDAK ADA KONEKSI INTERNET.")
    exit()

def get_location_coordinate(location_name):
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(location_name)
        return (location.latitude, location.longitude)
    except exc.GeocoderTimedOut:
        print("Waktu koneksi habis saat mencoba mengakses server")
        return None
    except exc.GeocoderUnavailable:
        print("Tidak ada koneksi internet")
        return None

# Membuat DataFrame kosong untuk menampung hasil perhitungan jarak
hasil_df = pd.DataFrame(columns=["Kendaraan", "Lokasi A", "Lokasi B", "Jarak (meter)"])

# Membuat DataFrame kosong untuk menampung koordinat

dflatlon = pd.DataFrame(columns=["Latitude A", "Longitude A", "Latitude B", "Longitude B" , "Kendaraan"])

# Inisialisasi geolocator
geolocator = Nominatim(user_agent="my_app")

def hitung_jarak():
    # Meminta input pengguna untuk nama kota atau daerah A
    location_a_name = input("Masukkan nama kota atau daerah A: ")
    location_a = geolocator.geocode(f"{location_a_name}, Indonesia")

    # Meminta input pengguna untuk nama kota atau daerah B
    location_b_name = input("Masukkan nama kota atau daerah B: ")
    location_b = geolocator.geocode(f"{location_b_name}, Indonesia")

    # Periksa apakah lokasi ditemukan atau tidak
    if not location_a or not location_b:
        print("Lokasi tidak ditemukan. Coba masukkan nama yang berbeda.")
        return

    # Dapatkan koordinat dari lokasi
    lat_a, lon_a = location_a.latitude, location_a.longitude
    lat_b, lon_b = location_b.latitude, location_b.longitude

    # API key untuk OpenRouteService
    api_key = '5b3ce3597851110001cf624848043e7128fc4b788ceee94c30167552'

    # Meminta input pengguna untuk memilih kendaraan
    vehicle = input("Pilih kendaraan (car/bike): ")

    if vehicle == "car":
        # URL API OpenRouteService untuk pengukuran jarak dan rute dengan car
        url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={lon_a},{lat_a}&end={lon_b},{lat_b}"
    elif vehicle == "bike":
        # URL API OpenRouteService untuk pengukuran jarak dan rute dengan pejalan bike
        url = f"https://api.openrouteservice.org/v2/directions/cycling-regular?api_key={api_key}&start={lon_a},{lat_a}&end={lon_b},{lat_b}"
    else:
        print("Kendaraan tidak dikenal.")
        return

    # Mengirim permintaan HTTP GET ke API OpenRouteService
    response = requests.get(url)

    # Mendeskripsikan nama file berdasarkan kota yang dicari
    iteration = location_a_name + ' ke ' + location_b_name

    # Mengecek status code respons HTTP
    if response.status_code == 200:
        print("Permintaan berhasil dilakukan.")
    else:
        print("Koneksi Internet Buruk.")
        return

    # Mengecek struktur respons JSON
    data = response.json()

    # Mendapatkan koordinat rute
    coordinates = data['features'][0]['geometry']['coordinates']

    # Membuat objek peta dengan library Folium
    map_route = folium.Map(location=[lat_a, lon_a], zoom_start=13)

    # Membuat objek polyline pada peta
    polyline = folium.PolyLine(
        locations=coordinates,
        weight=10,
        color='blue',
        opacity=1,
        smooth_factor=0
    ).add_to(map_route)

    # Menambahkan pin point untuk titik awal
    folium.Marker(
        location=[lat_a, lon_a],
        icon=folium.Icon(color='green', icon='play')
    ).add_to(map_route)

    # Menambahkan pin point untuk titik akhir
    folium.Marker(
        location=[lat_b, lon_b],
        icon=folium.Icon(color='red', icon='stop')
    ).add_to(map_route)

    # Nama folder baru
    folder_name = 'Geojsontiaprute'

    # Memeriksa apakah folder sudah ada atau tidak
    if not os.path.exists(folder_name):
        # Membuat folder baru jika folder belum ada
        os.mkdir(folder_name)

    # Menyimpan file dalam folder baru
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "marker-color": "#00ff00",
                    "marker-symbol": "play"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon_a, lat_a]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "marker-color": "#ff0000",
                    "marker-symbol": "stop"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon_b, lat_b]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "stroke": "#FF0000",
                    "stroke-width": 10
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": coordinates
                }
            }
        ]
    }

    with open(os.path.join(folder_name, f'route_{iteration}.geojson'), 'w') as f:
        json.dump(geojson_data, f)

    if 'features' in data and data['features']:
        print("Rute tersedia.")
    else:
        print("Rute tidak tersedia.")
        return

    # Mengambil jarak dari titik A ke B dalam meter
    distance = data['features'][0]['properties']['segments'][0]['distance']

    # Menampilkan jarak
    jarak = distance
    print(f"Jarak dari {location_a_name} ke {location_b} dengan {vehicle} adalah {jarak} meter.")

    # Menambahkan hasil jarak ke dalam DataFrame
    hasil_df.loc[len(hasil_df)] = [vehicle, location_a_name, location_b_name, jarak]

    # Menuliskan hasil ke dalam file Excel
    hasil_df.to_excel("Rekapitulasi jarak.xlsx", index=False)

    # Mengambil nama jalan yang dilewati rute
    road_names = []
    for segment in data['features'][0]['properties']['segments']:
        for step in segment['steps']:
            if 'name' in step:
                road_names.append(step['name'])

    # Menambahkan hasil jarak ke dalam DataFrame
    hasil_jalan_iterasi = pd.DataFrame(columns=['nama jalan'])
    for road_name in road_names:
        row = {'nama jalan': road_name}
        hasil_jalan_iterasi = hasil_jalan_iterasi._append(row, ignore_index=True)

    # Menampilkan nama jalan
    print(f"Tiga nama jalan pertama yang dilewati rute {iteration}:")

    for i in range(3):
        print(road_names[i])

    # Buat DataFrame dari list nama jalan
    nama_file = f"jalan {iteration}.xlsx"
    hasil_jalan_iterasi.to_excel(nama_file)
    print(f"Nama jalan telah disimpan dalam file {nama_file}:")

# Mengulang kode
while True:
    hitung_jarak()
    ulangi = input("Apakah Anda ingin mengulang? (y/n): ")
    if ulangi.lower() != 'y':
        break

lanjutkan_penggabungan_rute = input("Apakah Anda ingin menggabungkan semua rute? (y/n): ")
if lanjutkan_penggabungan_rute.lower() == 'y':
    # membuat variabel untuk nama folder baru
    folder_name = 'gabungan_rute'

    # path folder yang berisi file-file GeoJSON yang akan digabungkan
    folder_path = r"D:\pythonProject\Geojsontiaprute"

    # list file GeoJSON di dalam folder
    file_list = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.geojson')]

    # gabungkan semua file
    features = []
    for file in file_list:
        with fiona.open(file, 'r') as src:
            # baca schema dan crs dari file pertama
            if not features:
                schema = src.schema
                crs = src.crs

            # tambahkan semua features ke list features
            features += list(src)

        # membuat folder baru
        new_folder = os.path.join(folder_path, folder_name)
        os.makedirs(new_folder, exist_ok=True)

        # menuliskan hasil penggabungan ke file baru di dalam folder baru
        output_file = os.path.join(new_folder, 'hasil_gabungan.geojson')
        with fiona.open(output_file, 'w', driver='GeoJSON', schema=schema, crs=crs) as dst:
            for feature in features:
                dst.write(feature)
else:
    print("Penggabungan Rute selesai.")

lanjutkan_pencetakan_peta = input("Apakah Anda ingin mencetak peta? (y/n): ")
if lanjutkan_pencetakan_peta.lower() == 'y':

    # Tentukan path folder
    path = 'D:\pythonProject\Geojsontiaprute\gabungan_rute'

    # Cari file GeoJSON di folder
    geojson_files = glob.glob(os.path.join(path, '*.geojson'))

    # Baca file GeoJSON pertama yang ditemukan
    with open(geojson_files[0]) as f:
        geojson_data = json.load(f)

    # Buat peta
    m = folium.Map(location=[-7.6145, 110.7121], zoom_start=7)

    # Tambahkan layer GeoJSON
    folium.GeoJson(geojson_data).add_to(m)

    # Tambahkan tampilan tematik
    folium.LayerControl().add_to(m)

    # Simpan peta sebagai file HTML dalam folder baru
    folder_name = 'Peta_Baru'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_path = os.path.join(folder_name, 'peta gabungan.html')
    m.save(file_path)

else:
    print("Cetak Peta Selesai.")