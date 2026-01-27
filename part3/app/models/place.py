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
        
        # Validate before setting
        self.title = self.validate_title(title)
        self.description = self.validate_description(description)
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner_id = owner_id
        self.reviews = []  # List of review IDs
        self.amenities = []  # List of amenity IDs
    
    @staticmethod
    def validate_title(title):
        """Validate title."""
        if not title or not isinstance(title, str):
            raise ValueError("Title is required and must be a string")
        if len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(title) > 100:
            raise ValueError("Title must be less than 100 characters")
        return title.strip()
    
    @staticmethod
    def validate_description(description):
        """Validate description."""
        if not description or not isinstance(description, str):
            raise ValueError("Description is required and must be a string")
        if len(description.strip()) == 0:
            raise ValueError("Description cannot be empty")
        return description.strip()
    
    @staticmethod
    def validate_price(price):
        """Validate price."""
        try:
            price = float(price)
        except (ValueError, TypeError):
            raise ValueError("Price must be a number")
        
        if price <= 0:
            raise ValueError("Price must be positive")
        
        return price
    
    @staticmethod
    def validate_latitude(latitude):
        """Validate latitude."""
        try:
            latitude = float(latitude)
        except (ValueError, TypeError):
            raise ValueError("Latitude must be a number")
        
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        
        return latitude
    
    @staticmethod
    def validate_longitude(longitude):
        """Validate longitude."""
        try:
            longitude = float(longitude)
        except (ValueError, TypeError):
            raise ValueError("Longitude must be a number")
        
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        
        return longitude
    
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
