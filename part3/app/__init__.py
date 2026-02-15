"""
Flask application factory for HBnB.
"""
from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config
from app.models.db import db


def create_app(config_name='development'):
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    
    # Load configuration from config object
    app.config.from_object(config[config_name])
    
    # Initialize database
    db.init_app(app)
    
    # Create tables and initial data
    with app.app_context():
        db.create_all()
        
        # Check if admin exists, if not create it
        from app.models.user import User
        admin = User.query.filter_by(email='admin@hbnb.com').first()
        
        if not admin:
            admin = User(
                first_name='Admin',
                last_name='User',
                email='admin@hbnb.com',
                password='secret123',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created: admin@hbnb.com / secret123")
    
    # Enable CORS
    CORS(app)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize Flask-RESTX
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )
    
    # Register namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns
    
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    
    return app