from Car import Car
import time
import threading

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from ScanResult import ScanResult


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

    scanInterval = 0.5
    scanResult = ScanResult(scanInterval)

    while current_thread.read_dists:
        dists = car.read_distances()

        scanResult.add(dists)

        # emit('distances_car', {'front':dists[0], 'side': dists[1], 'back':dists[2]})
        print("Front = %.1f cm, Side = %.1f cm, Back = %.1f cm" % dists)
        time.sleep(scanInterval)

    print("Number of scans: " + str(scanResult.no_scans()) + " ")

    objects = scanResult.collect_objects()
    for obj in objects:
        print('Start index: ' + str(obj.start_index) + ' End index: ' + str(obj.end_index))

read_dists_thread = threading.Thread(target=read_dists_worker)
read_dists_thread.read_dists = False

@socket_io.on('forward_car',namespace='/test')
def forward_car(message):
    global read_dists_thread
    print('Moving car forward...')
    car.move_forward()

    if read_dists_thread.isAlive():
        print('Already reading distances...')
    else:
        read_dists_thread = threading.Thread(target=read_dists_worker)
        read_dists_thread.read_dists = True
        read_dists_thread.start()



@socket_io.on('backward_car',namespace='/test')
def backward_car(message):
    global read_dists_thread
    print('Moving car backward...')
    car.move_backward()

    if read_dists_thread.isAlive():
        print('Already reading distances...')
    else:
        read_dists_thread = threading.Thread(target=read_dists_worker)
        read_dists_thread.read_dists = True
        read_dists_thread.start()


@socket_io.on('stop_car',namespace='/test')
def stop(message):
    print('Stopping car...')
    car.stop()

    read_dists_thread.read_dists = False

    read_dists_thread.join()
    print('Successfully stopped reading distances...')



if __name__ == "__main__":
    try:
        socket_io.run(app,host='0.0.0.0')
    finally:
        car.cleanup()