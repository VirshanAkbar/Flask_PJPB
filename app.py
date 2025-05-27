from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask import jsonify
import eventlet
# from datetime import datetime
import csv
# import os

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app)

# CSV_FILE = './WebServerProto/sensor_data.csv'

# Create CSV file with headers if it doesn't exist
# if not os.path.exists(CSV_FILE):
#     with open(CSV_FILE, mode='w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(['timestamp', 'temperature (°C)', 'humidity (%)'])

@app.route('/')
def index():
    return "<h1> Hapunten, Euweuh Website! </h1>"
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload():
#     try:
#         temperature = request.form.get('temperature')
#         humidity = request.form.get('humidity')

#         if temperature is None or humidity is None:
#             return "Missing fields", 400

#         # Log to CSV
#         timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         with open(CSV_FILE, mode='a', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow([timestamp, temperature, humidity])

#         # Broadcast via WebSocket
#         socketio.emit('sensor_data', {
#             'temperature': temperature,
#             'humidity': humidity,
#             'timestamp': timestamp
#         })

#         return "Data received", 200

#     except Exception as e:
#         print("Error in /upload:", str(e))
#         return "Server error", 500

# @app.route('/api/data', methods=['GET'])
# def api_data():
#     try:
#         data = []
#         with open(CSV_FILE, mode='r') as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 data.append(row)
#         return jsonify(data)
#     except Exception as e:
#         print("Error in /api/data:", str(e))
#         return jsonify({'error': 'Could not read data'}), 500

# @app.route('/api/latest', methods=['GET'])
# def api_latest():
    try:
        with open(CSV_FILE, mode='r') as f:
            reader = list(csv.DictReader(f))
            if not reader:
                return jsonify({'error': 'No data available'}), 404
            latest = reader[-1]
        return jsonify(latest)
    except Exception as e:
        print("Error in /api/latest:", str(e))
        return jsonify({'error': 'Could not read data'}), 500

user_list = ["Adhy", "Rayhan", "Wimpi", "Virshan", "oye123"] #List dari User yang available, belum ada login atau autentikasi

lock_state = 0

# state int(0) -> unlock
# state int(1) -> lock

@app.route('/<username>/lock', methods=['GET'])
def get_lock_state(username):
    if username in user_list:
        return f"{lock_state}"
    else:
        return "User Not Found!"

# @app.route('/<username>/lock/locking', methods=['GET'])
# def turn_lock_on(username):
#     if username in user_list:
#         global lock_state
#         lock_state = "on"
#         return "Lock!"
#     else:
#         return "User Not Found!"

# @app.route('/<username>/lock/unlock', methods=['GET'])
# def turn_lock_off(username):
#     if username in user_list:
#         global lock_state
#         lock_state = "off"
#         return "Unlock!"
#     else:
#         return "User Not Found!"

@app.route('/<username>/lock/status', methods=['POST', 'GET'])
def status_lock(username):
    if username in user_list:
        global lock_state
        if (lock_state == 1):
            return f"{lock_state}"
        elif (lock_state == 0):
            return f"{lock_state}"
        else:
            return "Ngawur!"
    else:
        return "User Not Found!"
    

@app.route('/<username>/lock/locking', methods=['GET', 'POST'])
def lock(username):
    global lock_state
    if username in user_list:
        if request.method == 'POST':
            state = request.form.get('state')
            if state not in ['0', '1']:
                return jsonify({"error": "Invalid state, use 0 for unlock or 1 for lock"}), 400

            lock_state = int(state)
            print(f"Lock is now {'LOCKED' if lock_state else 'UNLOCKED'}")
            return jsonify({"status": f"Lock is now {'LOCKED' if lock_state else 'UNLOCKED'}"}), 200

        elif request.method == 'GET':
            return jsonify({"state": lock_state})  # 0 = unlocked, 1 = locked
    else:
        return "Ngawur!!"




if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
