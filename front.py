import streamlit as st
import requests
import time
import os
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

API_DATA     = "http://127.0.0.1:5000/data"
API_IMAGE    = "http://127.0.0.1:5000/image"

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

data_placeholder = st.empty()
map_placeholder = st.empty()
plot_placeholder = st.empty()
image_placeholder = st.empty()

def tampilan_awal():
    st.markdown('<div class="title"> BARELANG </div>', unsafe_allow_html=True)
    st.markdown('<div class="title"> MARINE ROBOTICS TEAM </div>', unsafe_allow_html=True)

def data():
    
    response = requests.get(API_DATA)  # Mengambil data dari backend Flask
    if response.status_code == 200:
        data = response.json()
        position = response.json()

        with data_placeholder.container():

            st.markdown('<div class="title_poltek"> POLITEKNIK NEGERI BATAM </div>', unsafe_allow_html=True)
            st.markdown('')

            c1, c2 = st.columns(2)

            with c1:
                st.markdown('<div class="label_tujuan"> GEO-TAG INFO </div>', unsafe_allow_html=True)

            with c2:
                st.markdown(f'''<div class="label_tujuan"> Position : {position['Position']} </div>''', unsafe_allow_html=True)
   
            col1, spacer1, col2, spacer2, col3, spacer3, col4 = st.columns([1, 0.2, 1, 0.2, 1, 0.2, 1])

            with col1:
                st.markdown(f'''
                <div class="lingkaran">
                    <div class="label">Day</div>
                    <div class="value">{data['Day']}</div>
                </div>''', unsafe_allow_html=True)

            with col2:
                st.markdown(f'''
                <div class="lingkaran">
                    <div class="label">Time</div>
                    <div class="value">{data['Time']}</div>
                </div>''', unsafe_allow_html=True)
                
            with col3:
                st.markdown(f'''
                <div class="lingkaran">
                    <div class="label">SOG [Knot]</div>
                    <div class="value">{data['SOG [Knot]']}</div>
                </div>''', unsafe_allow_html=True)

            with col4:
                st.markdown(f'''
                <div class="lingkaran">
                    <div class="label">SOG [Km/h]</div>
                    <div class="value">{data['SOG [Km/h]']}</div>
                </div>''', unsafe_allow_html=True)

            col1, spacer1, col2, spacer2, col3 = st.columns([1, 0.2, 1, 0.2, 1])

            with col1:
                st.markdown(f'''
                <div class="lingkaran">
                    <div class="label">Date</div>
                    <div class="value">{data['Date']}</div>
                </div>''', unsafe_allow_html=True)

            with col2:
                st.markdown(f'''
                <div class="lingkaran">
                    <div class="label">COG</div>
                    <div class="value">{data['COG']}°</div>
                </div>''', unsafe_allow_html=True)

            with col3:
                st.markdown(f'''
                <div class="lingkaran">
                    <div class="label">Coordinates</div>
                    <div class="value">{data['Coordinates']}</div>
                </div>''', unsafe_allow_html=True)
               
        return position['Position']
    else:
        st.error("Gagal mengambil data dari server!")
        return None

trajectory_a = [(2180, 100)]
def trajectory_map_a(position):

    if position:
        trajectory_a.append(position)

        trajectory_data_hijau = [
            (320, 980),  # Titik awal
            (320, 1320),
            (450, 1720),
            (1030, 2250),
            (1200, 2250),
            (1370, 2250),
            (1540, 2250),
            (2330, 1380),
            (2180, 1170),
            (2270, 870),
        ]
        x1, y1 = zip(*trajectory_data_hijau)
        trajectory_data_merah = [
            (170, 980),  # Titik awal
            (170, 1320),
            (300, 1720),
            (1030, 2100),
            (1200, 2100),
            (1370, 2100),
            (1540, 2100),
            (2180, 1380),
            (2030, 1170),
            (2120, 870),
        ]
        x2, y2 = zip(*trajectory_data_merah)

        trajectory_data_kotak_biru = [(580, 320),]
        x_biru, y_biru = zip(*trajectory_data_kotak_biru)

        trajectory_data_kotak_hijau = [(350, 650),]
        x_hijau, y_hijau = zip(*trajectory_data_kotak_hijau)

        trajectory_data_kotak_merah = [(2180, 100),]
        x_merah, y_merah = zip(*trajectory_data_kotak_merah)

        x_vals, y_vals = zip(*trajectory_a)

        # Membuat plot
        plt.figure(figsize=(15, 15))
        plt.scatter(x1, y1, color='green', s=200)  # titik hijau
        plt.scatter(x2, y2, color='red', s=200)  # titik merah
        plt.plot(x_vals, y_vals, marker='o', linestyle='-', color='blue')

        # Menggambar persegi panjang untuk titik hijau
        for (x, y) in zip(x_hijau, y_hijau):
            plt.gca().add_patch(plt.Rectangle((x - 50, y - 25), 100, 50, color='green'))  # Persegi panjang hijau

        # Menggambar persegi panjang untuk titik biru
        for (x, y) in zip(x_biru, y_biru):
            plt.gca().add_patch(plt.Rectangle((x - 50, y - 25), 100, 50, color='blue'))  # Persegi panjang biru

        # Menggambar persegi panjang untuk titik merah
        for (x, y) in zip(x_merah, y_merah):
            plt.gca().add_patch(plt.Rectangle((x - 80, y - 40), 160, 80, color='red'))  # Persegi panjang merah

        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.grid()
        plt.xlim(0, 2500)
        plt.ylim(0, 2500)

        # Menampilkan ticks setiap 200 pada sumbu x dan y
        plt.xticks(range(0, 2501, 100))  # Ticks pada sumbu x setiap 200
        plt.yticks(range(0, 2501, 100))  # Ticks pada sumbu y setiap 200

        plot_placeholder.pyplot(plt)

        # Menampilkan plot di Streamlit
        with map_placeholder.container():
            st.markdown('')
            st.markdown('<div class="label_tujuan"> Trajectory A </div>', unsafe_allow_html=True)

trajectory_b = [(340, 100)]
def trajectory_map_b(position):

    if position:
        trajectory_b.append(position)

        trajectory_data_hijau = [
            (240, 870),  # Titik awal
            (320, 1170),
            (180, 1480),
            (990, 2250),
            (1140, 2250),
            (1290, 2250),
            (1440, 2250),
            (2050, 1720),
            (2180, 1320),
            (2180, 970),
        ]
        # Memis0ahkan data menjadi dua list: x dan y
        x1, y1 = zip(*trajectory_data_hijau)

        trajectory_data_merah = [
            (390, 870),  # Titik awal
            (470, 1170),
            (330, 1480),
            (990, 2100),
            (1140, 2100),
            (1290, 2100),
            (1440, 2100),
            (2200, 1720),
            (2330, 1320),
            (2330, 970),
        ]
        x2, y2 = zip(*trajectory_data_merah)

        trajectory_data_kotak_biru = [(1940, 320),]
        x_biru, y_biru = zip(*trajectory_data_kotak_biru)

        trajectory_data_kotak_hijau = [(2150, 650),]
        x_hijau, y_hijau = zip(*trajectory_data_kotak_hijau)

        trajectory_data_kotak_merah = [(340, 100),]
        x_merah, y_merah = zip(*trajectory_data_kotak_merah)

        x_vals, y_vals = zip(*trajectory_b)

        # Membuat plot
        plt.figure(figsize=(15, 15))
        plt.scatter(x1, y1, color='green', s=200)  # titik hijau
        plt.scatter(x2, y2, color='red', s=200)  # titik merah
        plt.plot(x_vals, y_vals, marker='o', linestyle='-', color='blue')

        # Menggambar persegi panjang untuk titik hijau
        for (x, y) in zip(x_hijau, y_hijau):
            plt.gca().add_patch(plt.Rectangle((x - 50, y - 25), 100, 50, color='green'))  # Persegi panjang hijau

        # Menggambar persegi panjang untuk titik biru
        for (x, y) in zip(x_biru, y_biru):
            plt.gca().add_patch(plt.Rectangle((x - 50, y - 25), 100, 50, color='blue'))  # Persegi panjang biru

        # Menggambar persegi panjang untuk titik merah
        for (x, y) in zip(x_merah, y_merah):
            plt.gca().add_patch(plt.Rectangle((x - 80, y - 40), 160, 80, color='red'))  # Persegi panjang merah

        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.grid()
        plt.xlim(0, 2500)
        plt.ylim(0, 2500)

        # Menampilkan ticks setiap 200 pada sumbu x dan y
        plt.xticks(range(0, 2501, 100))  # Ticks pada sumbu x setiap 200
        plt.yticks(range(0, 2501, 100))  # Ticks pada sumbu y setiap 200

        plot_placeholder.pyplot(plt)

        # Menampilkan plot di Streamlit
        with map_placeholder.container():
            st.markdown('')
            st.markdown('<div class="label_tujuan"> Trajectory B </div>', unsafe_allow_html=True)

def gambar():
    response = requests.get(API_IMAGE)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        with image_placeholder.container():

            st.markdown('')
            st.markdown('<div class="label_tujuan"> Water Surface Picture </div>', unsafe_allow_html=True)
            st.markdown('')

            st.markdown(
                f"""
                <div class="image-container">
                    <img src="{API_IMAGE}" alt="Gambar di Tengah">
                </div>
                """,
                unsafe_allow_html=True)
    else:
        st.error("Failed to load image")


st.sidebar.markdown('<div class="title_sidebar"> Track Navigation </div>', unsafe_allow_html=True)
st.sidebar.markdown('')
spacer1, col1, spacer2, col2, spacer3 = st.sidebar.columns([0.5, 1, 0.3, 1, 0.5])

def sidebar():
    with col1:
        st.button("A", key="lintasan_a_button")

    with col2:
        st.button("B", key="lintasan_b_button")

    # Cek tombol yang ditekan
    if st.session_state.get("lintasan_a_button"):
        while True:
            position = data()
            trajectory_map_a(position)
            gambar()
            time.sleep(1)

    elif st.session_state.get("lintasan_b_button"):
        while True:
            position = data()
            trajectory_map_b(position)
            gambar()
            time.sleep(1)

    else:
        tampilan_awal()


sidebar()
