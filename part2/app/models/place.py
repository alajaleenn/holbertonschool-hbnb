from app.models.base_model import BaseModel


class Place(BaseModel):
    
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        """Initialize a Place instance."""
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []  
        self.amenities = []  
    
    def add_review(self, review_id):
        """Add a review to this place."""
        if review_id not in self.reviews:
            self.reviews.append(review_id)
    
    def add_amenity(self, amenity_id):
        """Add an amenity to this place."""
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)