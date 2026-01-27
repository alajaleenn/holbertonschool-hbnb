"""
BaseModel class - Parent class for all entities.
"""
import uuid
from datetime import datetime


class BaseModel:
    """
    Base class for all models.
    
    Attributes:
        id (str): Unique identifier
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
    """
    
    def __init__(self):
        """Initialize a new BaseModel instance."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def save(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """Convert object to dictionary."""
        obj_dict = {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        return obj_dict