from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__, static_folder="static")
CORS(app)

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.route("/data")
def get_data():
    if request.args.get("after") != None:
        time_filter = datetime.strptime(request.args.get("after"), '%d.%m.%Y').date()
    else:
        time_filter = None

    city_filter = request.args.get("city")

    conn = sqlite3.connect("qrdata.db")
    cursor = conn.cursor()

    query = "SELECT id, city, text, quantity, timestamp FROM qr_codes"
    params = []

    if time_filter != None:
        query += " WHERE timestamp <= ?"
        params.append(time_filter.strftime('%d.%m.%Y'))
        
    if city_filter:
        query += " AND city = ?"
        params.append(city_filter)
    
    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()

        return jsonify([
            {"id": row[0], "city": row[1], "text": row[2], "quantity": row[3], "timestamp": row[4]}
            for row in rows
        ])
    except sqlite3.OperationalError:
        return jsonify({})
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
