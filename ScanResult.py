class ScanResult:
    def __init__(self, readInterval, car2SideDistance = 50.0):
        self.scans = []
        self.readInterval = readInterval
        self.card2SideDistance = car2SideDistance

    def add(self,dists):
        self.scans.append(dists)

    def no_scans(self):
        return len(self.scans)

    def collect_objects(self):
        inventory_objects = []
        current_object = None

        for i in range(len(self.scans)):
            dists = self.scans[i]
            side_length = dists[1]

            if current_object is None:
                if abs(self.card2SideDistance - side_length) > 0.1 * self.card2SideDistance:
                    current_object = InventoryObject(i)
            else:
                if abs(self.card2SideDistance - side_length) < 0.1 * self.card2SideDistance:
                    current_object.end_index = i - 1
                    inventory_objects.append(current_object)
                    current_object = None

            if not(current_object is None):
                current_object.end_index = len(self.scans) - 1


        return inventory_objects





class InventoryObject:
    def __init__(self,start_index, end_index = -1):
        self.start_index = start_index
        self.end_index = end_index