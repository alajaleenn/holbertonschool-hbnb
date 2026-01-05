class InMemoryRepository:
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        if obj.id in self._storage:
            raise ValueError("Object already exists")
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, obj):
        if obj_id not in self._storage:
            raise KeyError("Object not found")
        self._storage[obj_id] = obj

    def delete(self, obj_id):
        if obj_id not in self._storage:
            raise KeyError("Object not found")
        del self._storage[obj_id]
