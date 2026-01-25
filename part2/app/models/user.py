"""
User model.
"""
from app.models.base_model import BaseModel
import re


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
        
        # Validate before setting
        self.first_name = self.validate_name(first_name, "First name")
        self.last_name = self.validate_name(last_name, "Last name")
        self.email = self.validate_email(email)
        self.is_admin = is_admin
    
    @staticmethod
    def validate_name(name, field_name):
        """Validate name fields."""
        if not name or not isinstance(name, str):
            raise ValueError(f"{field_name} is required and must be a string")
        if len(name.strip()) == 0:
            raise ValueError(f"{field_name} cannot be empty")
        if len(name) > 50:
            raise ValueError(f"{field_name} must be less than 50 characters")
        return name.strip()
    
    @staticmethod
    def validate_email(email):
        """Validate email format."""
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        
        # Simple email regex pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        
        return email.lower().strip()
    
    def to_dict(self):
        """Convert User to dictionary."""
        user_dict = super().to_dict()
        user_dict['first_name'] = self.first_name
        user_dict['last_name'] = self.last_name
        user_dict['email'] = self.email
        user_dict['is_admin'] = self.is_admin
        return user_dict
