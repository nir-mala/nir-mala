from flask import Flask, jsonify, send_file
from datetime import datetime
import random
from flask import Flask, send_file
import os

app = Flask(__name__)

IMAGE_FOLDER = os.getenv("IMAGE_FOLDER", r"E:\Users\Documents\Dewi\ular\trial\gambar tampil")

@app.route('/data', methods=['GET'])
def data():

    sog_knot = round(random.uniform(0, 100), 2)
    sog_kmh = round(sog_knot * 1.852, 2)
    latitude = round(random.uniform(-90, 0), 1)
    longitude = round(random.uniform(0, 180), 1)
    cog = round(random.uniform(0, 360), 2)

    x = random.randint(0, 2500)
    y = random.randint(0, 2500)

    now = datetime.now()

    current_day = now.strftime("%A")[:3]
    current_date = now.strftime("%Y/%m/%d")    
    current_time = now.strftime("%H:%M:%S")

    print(f"sog_knot : {sog_knot}, sog_kmh : {sog_kmh}", flush=True)
    print(f"Coordinates :S {latitude}° E {longitude}, cog : {cog}", flush=True)

    data = {
        "Day": current_day,
        "Date": current_date,
        "Time": current_time,
        "SOG [Knot]": sog_knot,
        "SOG [Km/h]": sog_kmh,
        "COG": cog,
        "Coordinates": f"S {latitude}° E {longitude}°",
        "Position": [x, y]
        }
    return jsonify(data)

    
@app.route('/image', methods=['GET'])
def get_image():
    image_path = os.path.join(IMAGE_FOLDER, "cat.jpg")
    return send_file(image_path, mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
