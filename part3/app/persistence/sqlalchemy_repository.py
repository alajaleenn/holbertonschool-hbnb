"""
SQLAlchemy Repository implementation.
"""
from typing import Type, List, Optional, Dict, Any
from app.models.db import db


class SQLAlchemyRepository:
    """Generic SQLAlchemy repository."""
    
    def __init__(self, model_class: Type[db.Model]):
        """Initialize with model class."""
        self.model_class = model_class
    
    def add(self, entity: db.Model) -> db.Model:
        """Add entity."""
        db.session.add(entity)
        db.session.commit()
        return entity
    
    def get(self, entity_id: Any) -> Optional[db.Model]:
        """Get by ID."""
        return self.model_class.query.get(entity_id)
    
    def get_all(self) -> List[db.Model]:
        """Get all entities."""
        return self.model_class.query.all()
    
    def update(self, entity_id: Any, data: Dict[str, Any]) -> Optional[db.Model]:
        """Update entity."""
        entity = self.get(entity_id)
        if not entity:
            return None
        
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        
        db.session.commit()
        return entity
    
    def delete(self, entity_id: Any) -> bool:
        """Delete entity."""
        entity = self.get(entity_id)
        if entity:
            db.session.delete(entity)
            db.session.commit()
            return True
        return False
    
    def get_by_attribute(self, attr_name: str, attr_value: Any) -> Optional[db.Model]:
        """Get by attribute."""
        return self.model_class.query.filter_by(**{attr_name: attr_value}).first()
