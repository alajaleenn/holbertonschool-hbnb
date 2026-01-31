"""
User SQLAlchemy model.
"""
import bcrypt
from app.models.db import db, BaseModel


class User(BaseModel):
    """User model with SQLAlchemy ORM."""
    
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relationships
    places = db.relationship('Place', backref='owner', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """Initialize User."""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email.lower()
        self.password = self.hash_password(password)
        self.is_admin = is_admin
    
    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password):
        """Verify password."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def to_dict(self):
        """Convert to dict (exclude password)."""
        user_dict = super().to_dict()
        user_dict.pop('password', None)
        return user_dict
