from flask import Flask, render_template
from flask_socketio import SocketIO
import time
from receiver import Receiver



app = Flask(__name__)
socketio = SocketIO(app)

class Server(SocketIO, Receiver):
    def __init__(self):
        super().__init__(app)
        self.Receiver.__init__()
        
        
    @app.route("/", methods=["GET", "POST"])
    def home(self):
        data = self.get_data()
        if data:
            temperature = data['temperature']
            humidity = data['humidity']

            return render_template("index.html", temperature=temperature,
                                                 humidity=humidity)
        else:
            return render_template("index.html", temperature=0,
                                                 humidity=0,)
    
    def start_server(self):
        socketio.run(app, host="0.0.0.0", port=8000, debug=True)
    

    @socketio.on('connect')
    def handle_connection(self):
        print('Socket connected')
        socketio.start_background_task(self.emit_data)
        #socketio.start_background_task(emit_video)
        
    def emit_data(self):
        while True:
            data = self.get_data()
            if data:
                temperature = data['temperature']
                humidity = data['humidity']

                socketio.emit('update', {'temperature': temperature,
                                         'humidity': humidity})
            time.sleep(2)



if __name__ == "__main__":
    server = Server()
    server.start_server()