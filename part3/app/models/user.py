cat > app/models/user.py << 'EOF'
"""
User SQLAlchemy model.
"""
import bcrypt
from app.models.db import db, BaseModel


class User(BaseModel):
    """
    User SQLAlchemy model.
    
    Attributes:
        first_name (str): User's first name
        last_name (str): User's last name
        email (str): User's email (unique)
        password (str): User's hashed password
        is_admin (bool): Admin status
    """
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    places = db.relationship('Place', backref='owner', lazy=True,
                           cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='author', lazy=True,
                            cascade='all, delete-orphan')
    
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
        # Remove password from response
        user_dict.pop('password', None)
        return user_dict
EOF
