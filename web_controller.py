from flask import render_template
from flask_socketio import emit
from storage_service import StorageService

class WebController:
    def __init__(self):
        self.storage_service = StorageService(self.publish_distances)

    def index(self):
        return render_template('index.html')

    def scan_storage(self, message):
        self.storage_service.scan_storage()

    def backward_car(self, message):
        self.storage_service.move_car_bwd()

    def stop_car(self, message):
        self.storage_service.stop_car()

    def publish_distances(self, front_dist, side_dist, back_dist):
        emit('car_distances', {'front': front_dist, 'side': side_dist, 'back': back_dist})