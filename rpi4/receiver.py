import serial
import time
import subprocess
import re
import json


subprocess.run(['sudo', 'systemctl', 'stop', 'serial-getty@ttyS0.service'])

class Receiver:
    def __init__(self):
        self.ser = serial.Serial('/dev/serial0', 9600, timeout=5)
        
    def get_data(self):
        while True:
            try:
                line = self.ser.readline().decode('utf-8')
                if line:
                    return json.loads(line)

            except serial.SerialException:
                print("could not receive data")

            except UnicodeDecodeError:
                time.sleep(0.1)
                continue