from Car import Car
import time
import threading

from flask import Flask, render_template
from flask_socketio import SocketIO, emit


car = Car(17, 18, 22, 23, 5, 6, 12, 13,
                  2, 3, 14, 15, 24, 25)


def test_move_car():
    try:
        car.move_forward()
        time.sleep(3)

        car.stop()
        time.sleep(0.5)

        car.move_backward()
        time.sleep(3)

        car.stop()
    except KeyboardInterrupt:
        print("... measurement stopped by user")



def test_read_sensor():
    try:
        distances = car.read_distances()
        print("Front = %.1f cm, Side = %.1f cm, Back = %.1f cm" % (distances[0], distances[1], distances[2]))
        time.sleep(1)
    except KeyboardInterrupt:
        print("... measurement stopped by user")



app = Flask(__name__)
app.config['SECRET_KEY']= 'secret'
socket_io = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')

def read_dists_worker():
    current_thread = threading.currentThread()
    print('Reading distances from thread: ' + current_thread.getName())
    while current_thread.read_dists:
        dists = car.read_distances()
        emit('distances_car', {'front':dists[0], 'side': dists[1], 'back':dists[2]})
        time.sleep(0.5)

read_dists_thread = threading.Thread(target=read_dists_worker)

@socket_io.on('forward_car',namespace='/test')
def forward_car(message):
    print('Moving car forward...')
    car.move_forward()

    if read_dists_thread.isAlive():
        print('Already reading distances...')
    else:
        read_dists_thread.read_dists = True
        read_dists_thread.run()



@socket_io.on('backward_car',namespace='/test')
def backward_car(message):
    print('Moving car backward...')
    car.move_backward()

@socket_io.on('stop_car',namespace='/test')
def stop(message):
    print('Stopping car...')
    car.stop()

    read_dists_thread.read_dists = False



if __name__ == "__main__":
    try:
        socket_io.run(app,host='0.0.0.0')
    finally:
        car.cleanup()