"""
Review model.
"""
from app.models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class.
    
    Attributes:
        text (str): Review text
        rating (int): Rating (1-5)
        place_id (str): Place ID
        user_id (str): User ID
    """
    
    def __init__(self, text, rating, place_id, user_id):
        """Initialize a Review instance."""
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
    
    def to_dict(self):
        """Convert Review to dictionary."""
        review_dict = super().to_dict()
        review_dict['text'] = self.text
        review_dict['rating'] = self.rating
        review_dict['place_id'] = self.place_id
        review_dict['user_id'] = self.user_id
        return review_dict
