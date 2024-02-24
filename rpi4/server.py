from flask import Flask, render_template
from flask_socketio import SocketIO
import time
from receiver import Receiver



app = Flask(__name__)
socketio = SocketIO(app)

receiver = Receiver()

def emit_data():
        while True:
            data = receiver.get_data()
            if data:
                temperature = data['temperature']
                humidity = data['humidity']

                socketio.emit('update', {'temperature': temperature,
                                         'humidity': humidity})
            time.sleep(2)


@app.route("/", methods=["GET", "POST"])
def home():
    data = receiver.get_data()
    if data:
        temperature = data['temperature']
        humidity = data['humidity']
        return render_template("index.html", temperature=temperature,
                                             humidity=humidity)
    else:
        return render_template("index.html", temperature=0,
                                             humidity=0)
        
        
@socketio.on('connect')
def handle_connection():
    print("client connected")
    socketio.start_background_task(emit_data)




def start_server():
    socketio.run(app, host="0.0.0.0", port=8050, debug=True)




if __name__ == "__main__":
    start_server()