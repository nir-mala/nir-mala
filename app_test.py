import streamlit as st
import requests
import time

# Konfigurasi Back4App
URL = "https://parseapi.back4app.com/classes/backend_trial"
HEADERS = {
    "X-Parse-Application-Id": "EvdYX9DzGQFfIjgNHLKitEtnPrc6f0Ebo7QkpcoV",
    "X-Parse-REST-API-Key": "I5p146Jcbyq1KKQZkLC4y1G4pY0De1RAR9rjUYVz",
    "Content-Type": "application/json"
}

st.title("🚀 Real-Time Data dari Back4App")

# Kontainer untuk streaming data
placeholder = st.empty()

# Loop untuk update data setiap 1 detik
while True:
    # Ambil data terbaru dari Back4App
    response = requests.get(URL, headers=HEADERS, params={
        "order": "-createdAt",  # Ambil data terbaru (sort by waktu)
        "limit": 1              # Hanya ambil data terbaru
    })

    if response.status_code == 200:
        data = response.json().get("results", [])
        if data:
            latest = data[0]
            placeholder.write(
                f"""
                ### Data Terbaru:
                - **Time:** {latest['Time']}
                - **Date:** {latest['Date']}
                - **Day:** {latest['Day']}
                - **COG:** {latest['COG']}
                - **SOG [Knot]:** {latest['SOG_Knot']}
                - **SOG [Km/h]:** {latest['SOG_kmperhours']}
                - **Lat:** {latest['Latitude']}
                - **Lon:** {latest['Longitude']}
                - **Position:** ({latest['Position_X']}, {latest['Position_Y']})
                """
            )
    else:
        st.warning(f"Error: {response.status_code}")

    # Tunggu 1 detik sebelum ambil data lagi
    time.sleep(1)
