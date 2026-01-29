cat > app/models/review.py << 'EOF'
"""
Review SQLAlchemy model.
"""
from app.models.db import db, BaseModel


class Review(BaseModel):
    """
    Review SQLAlchemy model.
    
    Attributes:
        text (str): Review text
        rating (int): Rating (1-5)
        place_id (str): Place ID (foreign key will be added later)
        user_id (str): User ID (foreign key will be added later)
    """
    __tablename__ = 'reviews'
    
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), nullable=False)  # Will become foreign key later
    user_id = db.Column(db.String(36), nullable=False)   # Will become foreign key later
    
    def __init__(self, text, rating, place_id, user_id):
        """Initialize a Review instance."""
        super().__init__()
        
        # Validate and set attributes
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place_id = place_id
        self.user_id = user_id
    
    @staticmethod
    def validate_text(text):
        """Validate review text."""
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string")
        if len(text.strip()) == 0:
            raise ValueError("Review text cannot be empty")
        if len(text) > 500:
            raise ValueError("Review text must be less than 500 characters")
        return text.strip()
    
    @staticmethod
    def validate_rating(rating):
        """Validate rating."""
        try:
            rating = int(rating)
        except (ValueError, TypeError):
            raise ValueError("Rating must be an integer")
        
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        
        return rating
    
    def to_dict(self):
        """Convert Review to dictionary."""
        review_dict = super().to_dict()
        return review_dict
EOF
