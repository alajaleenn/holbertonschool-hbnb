"""
SQLAlchemy Repository implementation.
"""
from app.models.db import db


class SQLAlchemyRepository:
    """Repository using SQLAlchemy for database operations."""
    
    def __init__(self, model_class):
        """Initialize with model class."""
        self.model_class = model_class
    
    def add(self, obj):
        """Add an object to database."""
        db.session.add(obj)
        db.session.commit()
        return obj
    
    def get(self, obj_id):
        """Get object by ID."""
        return self.model_class.query.get(obj_id)
    
    def get_all(self):
        """Get all objects."""
        return self.model_class.query.all()
    
    def update(self, obj_id, data):
        """Update object."""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            db.session.commit()
        return obj
    
    def delete(self, obj_id):
        """Delete object."""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False
    
    def get_by_attribute(self, attr_name, attr_value):
        """Get object by attribute value."""
        return self.model_class.query.filter(
            getattr(self.model_class, attr_name) == attr_value
        ).first()
    
    def get_all_by_attribute(self, attr_name, attr_value):
        """Get all objects by attribute value."""
        return self.model_class.query.filter(
            getattr(self.model_class, attr_name) == attr_value
        ).all()
