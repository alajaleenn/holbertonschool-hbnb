"""
Facade with SQLAlchemy repositories.
"""
from app.persistence.user_repository import UserRepository
from app.persistence.repository_factory import RepositoryFactory
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """Application facade."""
    
    def __init__(self):
        """Initialize facade."""
        self.user_repo = UserRepository()
        self.repo_factory = RepositoryFactory
    
    def _get_repo(self, model_name: str):
        """Get repository."""
        return self.repo_factory.get_repository(model_name)
    
    # USER METHODS
    def create_user(self, user_data: dict):
        return self.user_repo.create(user_data)
    
    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email: str):
        return self.user_repo.get_by_email(email)
    
    def get_all_users(self):
        return self.user_repo.get_all()
    
    def update_user(self, user_id, data: dict):
        return self.user_repo.update(user_id, data)
    
    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)
    
    def authenticate_user(self, email: str, password: str):
        return self.user_repo.authenticate(email, password)
    
    # PLACE METHODS
    def create_place(self, place_data: dict):
        place = Place(**place_data)
        return self._get_repo('Place').add(place)
    
    def get_place(self, place_id):
        return self._get_repo('Place').get(place_id)
    
    def get_all_places(self):
        return self._get_repo('Place').get_all()
    
    def update_place(self, place_id, data: dict):
        return self._get_repo('Place').update(place_id, data)
    
    def delete_place(self, place_id):
        return self._get_repo('Place').delete(place_id)
    
    # REVIEW METHODS
    def create_review(self, review_data: dict):
        review = Review(**review_data)
        return self._get_repo('Review').add(review)
    
    def get_review(self, review_id):
        return self._get_repo('Review').get(review_id)
    
    def get_all_reviews(self):
        return self._get_repo('Review').get_all()
    
    def update_review(self, review_id, data: dict):
        return self._get_repo('Review').update(review_id, data)
    
    def delete_review(self, review_id):
        return self._get_repo('Review').delete(review_id)
    
    def get_reviews_by_place(self, place_id):
        return self._get_repo('Review').get_by_attribute('place_id', place_id)
    
    # AMENITY METHODS
    def create_amenity(self, amenity_data: dict):
        amenity = Amenity(**amenity_data)
        return self._get_repo('Amenity').add(amenity)
    
    def get_amenity(self, amenity_id):
        return self._get_repo('Amenity').get(amenity_id)
    
    def get_all_amenities(self):
        return self._get_repo('Amenity').get_all()
    
    def update_amenity(self, amenity_id, data: dict):
        return self._get_repo('Amenity').update(amenity_id, data)
