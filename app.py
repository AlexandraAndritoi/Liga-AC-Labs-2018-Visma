from web_controller import WebController

from flask import Flask
from flask_socketio import SocketIO
import RPi.GPIO as GPIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_io = SocketIO(app)
#socket_io = SocketIO(app, logger=True, engineio_logger=True)


web_controller = WebController()
app.route('/')(web_controller.index)
socket_io.on('scan_storage')(web_controller.scan_storage)
socket_io.on('backward_car')(web_controller.backward_car)
socket_io.on('stop_car')(web_controller.stop_car)

if __name__ == "__main__":
    try:
        socket_io.run(app, host='0.0.0.0')
    finally:
        GPIO.cleanup()