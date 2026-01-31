"""
Models package for HBnB application.
"""
from app.models.db import db, BaseModel
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# Association table for Place-Amenity many-to-many relationship
place_amenity = db.Table("place_amenity",
    db.Column("place_id", db.String(36), db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"), primary_key=True),
    db.Column("created_at", db.DateTime, default=db.func.current_timestamp())
)

__all__ = ["db", "BaseModel", "User", "Place", "Review", "Amenity", "place_amenity"]
