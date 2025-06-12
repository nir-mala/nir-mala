# tampilan frontend dengan mengambil data melalui Back4APP
import streamlit as st
import requests
import time
import matplotlib.pyplot as plt


# Back4App config
URL = "https://parseapi.back4app.com/classes/backend_trial"
HEADERS = {
    "X-Parse-Application-Id": "EvdYX9DzGQFfIjgNHLKitEtnPrc6f0Ebo7QkpcoV",
    "X-Parse-REST-API-Key": "I5p146Jcbyq1KKQZkLC4y1G4pY0De1RAR9rjUYVz",
    "Content-Type": "application/json"
}

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Inisialisasi trajectory
if "trajectory" not in st.session_state:
    st.session_state.trajectory = []

placeholder = st.empty()

def monitoring():
    response = requests.get(URL, headers=HEADERS, params={
        "order": "-createdAt",
        "limit": 1
    })

    if response.status_code == 200:
        data = response.json().get("results", [])
        if data:
            latest = data[0]
            x = latest['Position_X']
            y = latest['Position_Y']
            point = (x, y)

            if not st.session_state.trajectory or st.session_state.trajectory[-1] != point:
                st.session_state.trajectory.append(point)

            with placeholder.container():
                st.markdown('<div class="title_poltek"> POLITEKNIK NEGERI BATAM </div>', unsafe_allow_html=True)                    
                st.markdown('')

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown('<div class="label_tujuan"> GEO-TAG INFO </div>', unsafe_allow_html=True)

                with c2:
                    st.markdown(f'''<div class="label_tujuan"> Position : ({point}) </div>''', unsafe_allow_html=True)

                col1, spacer1, col2, spacer2, col3, spacer3, col4 = st.columns([1, 0.2, 1, 0.2, 1, 0.2, 1])

                with col1:
                    st.markdown(f'''
                    <div class="lingkaran">
                        <div class="label">Day</div>
                        <div class="value">{latest['Day']}</div>
                    </div>''', unsafe_allow_html=True)

                with col2:
                    st.markdown(f'''
                    <div class="lingkaran">
                        <div class="label">Time</div>
                        <div class="value">{latest['Time']}</div>
                    </div>''', unsafe_allow_html=True)

                with col3:
                    st.markdown(f'''
                    <div class="lingkaran">
                        <div class="label">SOG [Knot]</div>
                        <div class="value">{latest['SOG_Knot']}</div>
                    </div>''', unsafe_allow_html=True)

                with col4:
                    st.markdown(f'''
                    <div class="lingkaran">
                        <div class="label">SOG [Km/h]</div>
                        <div class="value">{latest['SOG_kmperhours']}</div>
                    </div>''', unsafe_allow_html=True)

                col1, spacer1, col2, spacer2, col3 = st.columns([1, 0.2, 1, 0.2, 1])

                with col1:
                    st.markdown(f'''
                    <div class="lingkaran">
                        <div class="label">Date</div>
                        <div class="value">{latest['Date']}</div>
                    </div>''', unsafe_allow_html=True)

                with col2:
                    st.markdown(f'''
                    <div class="lingkaran">
                        <div class="label">COG</div>
                        <div class="value">{latest['COG']}°</div>
                    </div>''', unsafe_allow_html=True)

                with col3:
                    st.markdown(f'''
                    <div class="lingkaran">
                        <div class="label">Coordinates</div>
                        <div class="value">S {latest['Lattitude']}° E {latest['Longitude']}°</div>
                    </div>''', unsafe_allow_html=True)
    else:
        st.warning(f"Error: {response.status_code}")

def trajectory_A():
    if not st.session_state.trajectory:
        st.session_state.trajectory.append((2180, 100))
        
    x_vals, y_vals = zip(*st.session_state.trajectory)

    fig, ax = plt.subplots(figsize=(15, 15))
    ax.set_xticks(range(0, 2600, 100))
    ax.set_yticks(range(0, 2600, 100))
    ax.grid(True)

    # Titik referensi tetap
    hijau = [(320, 980), (320, 1320), (450, 1720), (1030, 2250), (1200, 2250), (1370, 2250),
            (1540, 2250), (2330, 1380), (2180, 1170), (2270, 870)]
    merah = [(170, 980), (170, 1320), (300, 1720), (1030, 2100), (1200, 2100), (1370, 2100),
            (1540, 2100), (2180, 1380), (2030, 1170), (2120, 870)]

    ax.scatter(*zip(*hijau), color='green', s=200)
    ax.scatter(*zip(*merah), color='red', s=200)

    # Tandai titik awal
    start_x, start_y = st.session_state.trajectory[0]
    ax.scatter(start_x, start_y, color='purple', s=300, label='Start')
    ax.text(start_x + 20, start_y + 20, 'Start', fontsize=12, color='purple')

    for x, y, color in [(580, 320, 'blue'), (350, 650, 'green'), (2180, 100, 'red')]:
        ax.add_patch(plt.Rectangle((x - 50, y - 25), 100, 50, color=color))

    ax.plot(x_vals, y_vals, marker='o', color='blue', linewidth=2)

    ax.set_title("Trajectory A")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_xlim(0, 2500)
    ax.set_ylim(0, 2500)
    ax.set_aspect('equal', adjustable='box')

    st.pyplot(fig)

# Jalankan
monitoring()
trajectory_A()


# Tunggu 3 detik lalu rerun otomatis
time.sleep(3)
st.rerun()