from storage_object import StorageObject
from time import time

class StorageScan:
    def __init__(self, storage_length, side_car_distance, scan_interval, start_time = time()):
        self._scan_dists = []
        self._storage_length = storage_length
        self._side_car_distance = side_car_distance
        self._scan_interval = scan_interval
        self._start_time = start_time

    def add_dists(self, dists):
        self._scan_dists.append(dists)

    def no_scan_dists(self):
        return len(self._scan_dists)

    def collect_objects(self):
        scan_objects = []
        current_scan_object = None

        for i in range(len(self._scan_dists)):
            dists = self._scan_dists[i]
            side_length = dists[1]

            if current_scan_object is None:
                if abs(self._side_car_distance - side_length) > 0.2 * self._side_car_distance:
                    current_scan_object = StorageObject(i)
            else:
                if abs(self._side_car_distance - side_length) <= 0.2 * self._side_car_distance:
                    end_index = i - 1
                    if current_scan_object.start_index == end_index:
                        # start_index == end_index => erroneous scan; discard scan_object
                        current_scan_object = None
                    else:
                        current_scan_object.end_index = end_index
                        scan_objects.append(current_scan_object)
                        current_scan_object = None

        if not(current_scan_object is None):
            current_scan_object.end_index = len(self._scan_dists) - 1
            scan_objects.append(current_scan_object)

        return scan_objects