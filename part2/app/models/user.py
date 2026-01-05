"""
User model.
"""
from app.models.base_model import BaseModel


class User(BaseModel):
    """
    User class.
    
    Attributes:
        first_name (str): User's first name
        last_name (str): User's last name
        email (str): User's email (unique)
        is_admin (bool): Admin status
    """
    
    def __init__(self, first_name, last_name, email, is_admin=False):
        """Initialize a User instance."""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
    
    def to_dict(self):
        """Convert User to dictionary."""
        user_dict = super().to_dict()
        user_dict['first_name'] = self.first_name
        user_dict['last_name'] = self.last_name
        user_dict['email'] = self.email
        user_dict['is_admin'] = self.is_admin
        return user_dict