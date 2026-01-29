echo '"""
Models package for HBnB application.
"""
from app.models.db import db, BaseModel
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

__all__ = ["db", "BaseModel", "User", "Place", "Review", "Amenity"]' > app/models/__init__.py
