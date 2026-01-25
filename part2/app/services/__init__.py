"""
Services package initialization.
"""
from app.services.facade import HBnBFacade

# Create a single shared facade instance
shared_facade = HBnBFacade()
