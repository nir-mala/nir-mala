import streamlit as st
import requests
import time
import os

# Konfigurasi Back4App
URL = "https://parseapi.back4app.com/classes/backend_trial"
HEADERS = {
    "X-Parse-Application-Id": "EvdYX9DzGQFfIjgNHLKitEtnPrc6f0Ebo7QkpcoV",
    "X-Parse-REST-API-Key": "I5p146Jcbyq1KKQZkLC4y1G4pY0De1RAR9rjUYVz",
    "Content-Type": "application/json"
}

# Pemuatan CSS di luar fungsi utama
css_path = os.path.join(os.getcwd(), "styles.css")  # Path ke file CSS eksternal

if os.path.exists(css_path):  # Cek apakah file CSS ada
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
# Kontainer untuk streaming data
placeholder = st.empty()

while True:
    response = requests.get(URL, headers=HEADERS, params={
        "order": "-createdAt",
        "limit": 1
    })
    
    if response.status_code == 200:
        data = response.json().get("results", [])
        if data:
            latest = data[0]
            with placeholder.container():
                st.markdown('<div class="title_poltek"> POLITEKNIK NEGERI BATAM </div>', unsafe_allow_html=True)
                st.markdown('')
    
                c1, c2 = st.columns(2)
    
                with c1:
                st.markdown('<div class="label_tujuan"> GEO-TAG INFO </div>', unsafe_allow_html=True)
    
                with c2:
                st.markdown(f'''<div class="label_tujuan"> Position : ({latest['Position_X']}, {latest['Position_Y']}) </div>''', unsafe_allow_html=True)
    
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
    
    time.sleep(1)

