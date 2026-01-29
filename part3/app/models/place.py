cat > app/models/place.py << 'EOF'
"""
Place SQLAlchemy model.
"""
from app.models.db import db, BaseModel


class Place(BaseModel):
    """
    Place SQLAlchemy model.
    
    Attributes:
        title (str): Place title
        description (str): Place description
        price (float): Price per night
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
        owner_id (str): Owner's user ID (foreign key will be added later)
    """
    __tablename__ = 'places'
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), nullable=False)  # Will become foreign key later
    
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        """Initialize a Place instance."""
        super().__init__()
        
        # Validate and set attributes
        self.title = self.validate_title(title)
        self.description = self.validate_description(description)
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner_id = owner_id
    
    @staticmethod
    def validate_title(title):
        """Validate title."""
        if not title or not isinstance(title, str):
            raise ValueError("Title is required and must be a string")
        if len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(title) > 100:
            raise ValueError("Title must be less than 100 characters")
        return title.strip()
    
    @staticmethod
    def validate_description(description):
        """Validate description."""
        if not description or not isinstance(description, str):
            raise ValueError("Description is required and must be a string")
        if len(description.strip()) == 0:
            raise ValueError("Description cannot be empty")
        return description.strip()
    
    @staticmethod
    def validate_price(price):
        """Validate price."""
        try:
            price = float(price)
        except (ValueError, TypeError):
            raise ValueError("Price must be a number")
        
        if price <= 0:
            raise ValueError("Price must be positive")
        
        return price
    
    @staticmethod
    def validate_latitude(latitude):
        """Validate latitude."""
        try:
            latitude = float(latitude)
        except (ValueError, TypeError):
            raise ValueError("Latitude must be a number")
        
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        
        return latitude
    
    @staticmethod
    def validate_longitude(longitude):
        """Validate longitude."""
        try:
            longitude = float(longitude)
        except (ValueError, TypeError):
            raise ValueError("Longitude must be a number")
        
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        
        return longitude
    
    def to_dict(self):
        """Convert Place to dictionary."""
        place_dict = super().to_dict()
        return place_dict
EOF
