"""
Amenity SQLAlchemy model.
"""
from app.models.db import db, BaseModel


class Amenity(BaseModel):
    """Amenity model."""
    
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __init__(self, name):
        """Initialize Amenity."""
        super().__init__()
        self.name = name
