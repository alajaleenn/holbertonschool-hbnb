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
        self.name = self.validate_name(name)
    
    @staticmethod
    def validate_name(name):
        """Validate amenity name."""
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name is required and must be a string")
        if len(name.strip()) == 0:
            raise ValueError("Amenity name cannot be empty")
        if len(name) > 50:
            raise ValueError("Amenity name must be less than 50 characters")
        return name.strip()
    
    def to_dict(self):
        """Convert Amenity to dictionary."""
        amenity_dict = super().to_dict()
        amenity_dict['name'] = self.name
        return amenity_dict
