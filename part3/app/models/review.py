cat > app/models/review.py << 'EOF'
from app.models.db import db, BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'
    
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place_id = place_id
        self.user_id = user_id
    
    @staticmethod
    def validate_text(text):
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string")
        if len(text.strip()) == 0:
            raise ValueError("Review text cannot be empty")
        if len(text) > 500:
            raise ValueError("Review text must be less than 500 characters")
        return text.strip()
    
    @staticmethod
    def validate_rating(rating):
        try:
            rating = int(rating)
        except (ValueError, TypeError):
            raise ValueError("Rating must be an integer")
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating
    
    def to_dict(self):
        return super().to_dict()
EOF
