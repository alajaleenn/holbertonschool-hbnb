cat > app/models/amenity.py << 'EOF'
"""
Amenity SQLAlchemy model.
"""
from app.models.db import db, BaseModel


class Amenity(BaseModel):
    """
    Amenity SQLAlchemy model.
    
    Attributes:
        name (str): Amenity name
    """
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __init__(self, name):
        """Initialize an Amenity instance."""
        super().__init__()
        self.name = self.validate_name(name)
    
    @staticmethod
    def validate_name(name):
        """Validate amenity name."""
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name is required and must be a string")
        if len(name.strip()) == 0:
            raise ValueError("Amenity name cannot be empty")
        if len(name) > 50:
            raise ValueError("Amenity name must be less than 50 characters")
        return name.strip()
    
    def to_dict(self):
        """Convert Amenity to dictionary."""
        amenity_dict = super().to_dict()
        return amenity_dict
EOF
