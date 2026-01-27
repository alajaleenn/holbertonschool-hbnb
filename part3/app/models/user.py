"""
User model.
"""
from app.models.base_model import BaseModel
import bcrypt


class User(BaseModel):
    """
    User class.
    
    Attributes:
        first_name (str): User's first name
        last_name (str): User's last name
        email (str): User's email (unique)
        password (str): User's hashed password
        is_admin (bool): Admin status
    """
    
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """Initialize a User instance."""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.hash_password(password)
        self.is_admin = is_admin
    
    def hash_password(self, password):
        """Hash a password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password):
        """Verify a password against the hashed password."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def to_dict(self):
        """Convert User to dictionary (excluding password)."""
        user_dict = super().to_dict()
        user_dict['first_name'] = self.first_name
        user_dict['last_name'] = self.last_name
        user_dict['email'] = self.email
        user_dict['is_admin'] = self.is_admin
        # IMPORTANT: Never include password in the response
        return user_dict