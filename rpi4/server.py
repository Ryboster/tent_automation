from flask import Flask, render_template
from flask_socketio import SocketIO
import time
from receiver import Receiver



app = Flask(__name__)
socketio = SocketIO(app)

receiver = Receiver()


#class Server(SocketIO, Receiver):
#    def __init__(self):
#        super().__init__(app)
#        Receiver.__init__(self)
#        
#        
#    @app.route("/", methods=["GET", "POST"])
#    def home():
#        data = Receiver().get_data()
#        if data:
#            temperature = data['temperature']
#            humidity = data['humidity']
#
#            return render_template("index.html", temperature=temperature,
#                                                 humidity=humidity)
#        else:
#            return render_template("index.html", temperature=0,
#                                                 humidity=0,)
#    
#    def start_server(self):
#        socketio.run(app, host="0.0.0.0", port=8000, debug=True)
#    
#
#    @socketio.on('connect')
#    def handle_connection():
#        print('Socket connected')
#        socketio.start_background_task(emit_data)
#        #socketio.start_background_task(emit_video)
#        
#    




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




def start_server(self):
    socketio.run(app, host="0.0.0.0", port=8050, debug=True)




if __name__ == "__main__":
    start_server()