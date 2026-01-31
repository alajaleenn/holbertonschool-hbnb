"""
Place SQLAlchemy model.
"""
from app.models.db import db, BaseModel

# Association table for Place-Amenity many-to-many
place_amenities = db.Table('place_amenities',
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel):
    """Place model."""
    
    __tablename__ = 'places'
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenities, lazy='subquery',
                               backref=db.backref('places', lazy=True))
    
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        """Initialize Place."""
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
