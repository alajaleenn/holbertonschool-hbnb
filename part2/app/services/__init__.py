"""
Services package.
"""
from app.services.facade import HBnBFacade

# Create a single shared instance of the facade
shared_facade = HBnBFacade()
