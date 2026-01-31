"""
Flask application factory.
"""
from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from app.models.db import db
from config import config


def create_app(config_name='development'):
    """Create Flask app."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Initialize API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/',
        authorizations={
            'Bearer Auth': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            }
        },
        security='Bearer Auth'
    )
    
    # Register namespaces
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.admin import api as admin_ns
    
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(admin_ns, path='/api/v1/admin')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
