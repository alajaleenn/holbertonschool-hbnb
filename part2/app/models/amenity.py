from app.models.base_model import BaseModel


class Amenity(BaseModel):
    
    def __init__(self, name):
        super().__init__()
        self.name = name

    def to_dict(self):
        """Convert Amenity to dictionary."""
        amenity_dict = super().to_dict()
        amenity_dict['name'] = self.name
        return amenity_dict
