from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
  
    
    def __init__(self):
        """Initialize facade with repository."""
        self.repository = InMemoryRepository()
    
    # User methods
    def create_user(self, user_data):
        """Create a new user."""
        user = User(**user_data)
        self.repository.add(user)
        return user
    
    def get_user(self, user_id):
        """Get user by ID."""
        return self.repository.get(user_id, 'User')
    
    def get_user_by_email(self, email):
        """Get user by email."""
        return self.repository.get_by_attribute('User', 'email', email)
    
    # Place methods
    def create_place(self, place_data):
        """Create a new place."""
        place = Place(**place_data)
        self.repository.add(place)
        return place
    
    def get_place(self, place_id):
        """Get place by ID."""
        return self.repository.get(place_id, 'Place')
    
    # Review methods
    def create_review(self, review_data):
        """Create a new review."""
        review = Review(**review_data)
        self.repository.add(review)
        
        # Add review to place
        place = self.get_place(review.place_id)
        if place:
            place.add_review(review.id)
        
        return review
    
    def get_review(self, review_id):
        """Get review by ID."""
        return self.repository.get(review_id, 'Review')
    
    def get_reviews_by_place(self, place_id):
        """Get all reviews for a place."""
        all_reviews = self.repository.get_all('Review')
        return [r for r in all_reviews if r.place_id == place_id]
    
    def delete_review(self, review_id):
        """Delete a review."""
        return self.repository.delete(review_id, 'Review')
    
    # Amenity methods
    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        amenity = Amenity(**amenity_data)
        self.repository.add(amenity)
        return amenity
    
    def get_amenity(self, amenity_id):
        """Get amenity by ID."""
        return self.repository.get(amenity_id, 'Amenity')
    def get_all_amenities(self):
        """Get all amenities."""
        return self.repository.get_all('Amenity')

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity."""
       return self.repository.update(amenity_id, 'Amenity', amenity_data)
   def get_all_places(self):
        """Get all places."""
        return self.repository.get_all('Place')

    def add_amenity_to_place(self, place_id, amenity_id):
        """Add an amenity to a place."""
        place = self.get_place(place_id)
        amenity = self.get_amenity(amenity_id)

        if not place:
            return None, 'Place not found'
        if not amenity:
            return None, 'Amenity not found'

        place.add_amenity(amenity_id)
        return place, None
