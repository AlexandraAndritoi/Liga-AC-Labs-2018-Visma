from threading import Thread
from functools import wraps
import time

from car.car import Car
from storage.storage_scan import StorageScan
from storage.storage_object import StorageObject

class StorageService:
    def __init__(self, publish_distances_func, publish_location_func):
        self.publish_distances_func = publish_distances_func
        self.publish_location_func = publish_location_func
        self.scan_interval = 0.25
        # self.car = Car(6, 13, 19, 26, 21, 20, 16, 12,
        #       14, 15, 18, 17, 2, 3)
        self.car = Car(17, 18, 22, 23, 5, 6, 12, 13,
                       2, 3, 14, 15, 24, 25)

        self.car_running = False

    def _return_back_car(self, start_time, end_time):
        print('Returning back the car ...')
        duration = end_time - start_time
        remaining_duration = end_time - start_time
        step = 0.2

        self.car.stop()
        time.sleep(step)

        self.car.move_backward()
        while remaining_duration > 0:
            remaining_duration = remaining_duration - step
            location = remaining_duration / duration
            print("Location: " + str(location))
            self.publish_location_func(location)
            time.sleep(step)

        self.car.stop()

    def _scan_storage_worker(self):
        storage_scan = StorageScan(210, 50, self.scan_interval)
        start_time = time.time()

        while self.car_running:
            dists = self.car.read_distances()
            emergency_stop_front = dists[3]
            storage_scan.add_dists((dists[0], dists[1], dists[2]))

            self.publish_distances_func(dists[0], dists[1], dists[2])

            # print("Front = %.2f cm, side = %.2f cm, back %.2f cm, emergency stop: %r" % dists)
            if emergency_stop_front:
                self.car.stop()
                break

            time.sleep(self.scan_interval)

        end_time = time.time()

        objects = storage_scan.collect_objects()
        print('Number of scans: ' + str(storage_scan.no_scan_dists()) + '; number of objects: ' + str(len(objects)))
        for obj in objects:
            print('Start index: ' + str(obj.start_index) + '; end index: ' + str(obj.end_index))

        self._return_back_car(start_time, end_time)



    def scan_storage(self):
        dists = self.car.read_distances()
        emergency_stop_front = dists[3]

        if emergency_stop_front:
            print('Too close to objects. Car not moving forward!')
            return

        self.car_running = True
        self.car.move_forward()

        #eventlet.spawn(self.read_dists_worker)
        self._scan_storage_worker()

    def move_car_bwd(self):
        self.car.move_backward()

    def stop_car(self):
        self.car_running = False
        self.car.stop()