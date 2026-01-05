class InMemoryRepository:
   
    
    def __init__(self):
        """Initialize empty storage."""
        self._storage = {}
    
    def add(self, obj):
        """Add an object to storage."""
        class_name = obj.__class__.__name__
        if class_name not in self._storage:
            self._storage[class_name] = {}
        self._storage[class_name][obj.id] = obj
        return obj
    
    def get(self, obj_id, obj_type):
        """Get an object by ID and type."""
        return self._storage.get(obj_type, {}).get(obj_id)
    
    def get_all(self, obj_type):
        """Get all objects of a type."""
        return list(self._storage.get(obj_type, {}).values())
    
    def update(self, obj_id, obj_type, data):
        """Update an object."""
        obj = self.get(obj_id, obj_type)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            obj.save()
            return obj
        return None
    
    def delete(self, obj_id, obj_type):
        """Delete an object."""
        if obj_type in self._storage and obj_id in self._storage[obj_type]:
            del self._storage[obj_type][obj_id]
            return True
        return False
    
    def get_by_attribute(self, obj_type, attr_name, attr_value):
        """Get object by attribute value."""
        objects = self.get_all(obj_type)
        for obj in objects:
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value:
                return obj
        return None