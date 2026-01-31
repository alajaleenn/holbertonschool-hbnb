"""
User-specific repository.
"""
from typing import Optional
from app.models.user import User
from app.models.db import db


class UserRepository:
    """Repository for User operations."""
    
    def __init__(self):
        """Initialize UserRepository."""
        self.model = User
    
    def create(self, user_data: dict) -> User:
        """Create user."""
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user
    
    def get(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.model.query.get(user_id)
    
    def get_all(self):
        """Get all users."""
        return self.model.query.all()
    
    def update(self, user_id: int, data: dict) -> Optional[User]:
        """Update user."""
        user = self.get(user_id)
        if not user:
            return None
        
        if 'password' in data:
            user.password = user.hash_password(data.pop('password'))
        
        for key, value in data.items():
            if hasattr(user, key) and key != 'id':
                setattr(user, key, value)
        
        db.session.commit()
        return user
    
    def delete(self, user_id: int) -> bool:
        """Delete user."""
        user = self.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get by email."""
        return self.model.query.filter_by(email=email.lower()).first()
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate user."""
        user = self.get_by_email(email)
        if user and user.verify_password(password):
            return user
        return None
