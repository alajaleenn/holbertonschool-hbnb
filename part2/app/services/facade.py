from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.repository = InMemoryRepository()

    def create(self, obj):
        self.repository.add(obj)
        return obj

    def get(self, obj_id):
        return self.repository.get(obj_id)

    def get_all(self):
        return self.repository.get_all()

    def delete(self, obj_id):
        self.repository.delete(obj_id)
