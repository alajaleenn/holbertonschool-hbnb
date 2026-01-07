"""
Place model.
"""
from app.models.base_model import BaseModel


class Place(BaseModel):
    """
    Place class.
    
    Attributes:
        title (str): Place title
        description (str): Place description
        price (float): Price per night
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
        owner_id (str): Owner's user ID
    """
    
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        """Initialize a Place instance."""
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []  # List of review IDs
        self.amenities = []  # List of amenity IDs
    
    def add_review(self, review_id):
        """Add a review to this place."""
        if review_id not in self.reviews:
            self.reviews.append(review_id)
    
    def add_amenity(self, amenity_id):
        """Add an amenity to this place."""
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)
    
    def to_dict(self):
        """Convert Place to dictionary."""
        place_dict = super().to_dict()
        place_dict['title'] = self.title
        place_dict['description'] = self.description
        place_dict['price'] = self.price
        place_dict['latitude'] = self.latitude
        place_dict['longitude'] = self.longitude
        place_dict['owner_id'] = self.owner_id
        place_dict['reviews'] = self.reviews.copy()
        place_dict['amenities'] = self.amenities.copy()
        return place_dict
