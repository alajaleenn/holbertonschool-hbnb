'EOF'
"""
Repository factory and interface.
"""
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class RepositoryFactory:
    """Factory to create repositories for different models."""
    
    @staticmethod
    def get_user_repository():
        """Get repository for User model."""
        return SQLAlchemyRepository(User)
    
    @staticmethod
    def get_place_repository():
        """Get repository for Place model."""
        return SQLAlchemyRepository(Place)
    
    @staticmethod
    def get_review_repository():
        """Get repository for Review model."""
        return SQLAlchemyRepository(Review)
    
    @staticmethod
    def get_amenity_repository():
        """Get repository for Amenity model."""
        return SQLAlchemyRepository(Amenity)


# Backward compatibility
class InMemoryRepository:
    """Legacy in-memory repository (for backward compatibility)."""
    
    def __init__(self):
        self._storage = {}
    
    def add(self, obj):
        class_name = obj.__class__.__name__
        if class_name not in self._storage:
            self._storage[class_name] = {}
        self._storage[class_name][obj.id] = obj
        return obj
    
    def get(self, obj_id, obj_type):
        return self._storage.get(obj_type, {}).get(obj_id)
    
    def get_all(self, obj_type):
        return list(self._storage.get(obj_type, {}).values())
    
    def update(self, obj_id, obj_type, data):
        obj = self.get(obj_id, obj_type)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            obj.save()
            return obj
        return None
    
    def delete(self, obj_id, obj_type):
        if obj_type in self._storage and obj_id in self._storage[obj_type]:
            del self._storage[obj_type][obj_id]
            return True
        return False
    
    def get_by_attribute(self, obj_type, attr_name, attr_value):
        objects = self.get_all(obj_type)
        for obj in objects:
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value:
                return obj
        return None
EOF
