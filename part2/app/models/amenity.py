"""
Amenity model.
"""
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity class.
    
    Attributes:
        name (str): Amenity name
    """
    
    def __init__(self, name):
        """Initialize an Amenity instance."""
        super().__init__()
        self.name = name
    
    def to_dict(self):
        """Convert Amenity to dictionary."""
        amenity_dict = super().to_dict()
        amenity_dict['name'] = self.name
        return amenity_dict
