from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO
import time

import cv2
import base64

import serial


from receiver import Receiver

#serial_port = '/dev/ttyS0'
#baud_rate = 9600
#ser = serial.Serial(serial_port, baud_rate)


app = Flask(__name__)
socketio = SocketIO(app)



class Server(socketio.Server, Receiver):
    def __init__(self):
        self.Receiver.__init__()
        self.ser = serial.Serial('/dev/ttyS0', 9600)
        
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        
    @app.route("/", methods=["GET", "POST"])
    def home(self):
        data = self.get_data()
        temperature = data['temperature']
        humidity = data['humidity']
        
        return render_template("index.html", temperature=temperature, humidity=humidity)
    
    


def emit_data():
    while True:
        hum, temp = read_dht_data()
        socketio.emit('update', {"temperature": temp, "humidity": hum})
        time.sleep(0.5)

def emit_video():
    pass
    #cap = cv2.VideoCapture('Cricket Bowling 150fps 1200.avi')
    #target_fps = 60
    #target_timeframe = 1 / target_fps
    #start_time = time.time()
#
    #while True:
#
    #    ret, frame = cap.read()
    #    if not ret:
    #        break
    #    print(f"ret: {ret}")
    #    print(f"frame {frame}")
#
    #    _, buffer = cv2.imencode(".png", frame)
    #    frame_encoded = base64.b64encode(buffer).decode('utf-8')
#
#base64.b64encode(buffer).decode('utf-8')

    #    socketio.emit("video", {"frame": frame_encoded})
#
    #    cap.release()
    #    time.sleep(1)



@app.route("/", methods=["GET", "POST"])
def home():
    data = Receiver().get_data()
    temperature = data['temperature']
    humidity = data['humidity']
    
    return render_template("index.html", temperature=temperature, humidity=humidity)



@socketio.on('connect')
def handle_connect():
    print('Socket connected')
    socketio.start_background_task(emit_data)
    #socketio.start_background_task(emit_video)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)