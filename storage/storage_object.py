class StorageObject:
    def __init__(self, start_index, storage_object_type = 'object', end_index = -1):
        self.storage_object_type = storage_object_type
        self.start_index = start_index
        self.end_index = end_index
        self.length = 0