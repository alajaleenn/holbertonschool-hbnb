"""
Repository factory.
"""
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class RepositoryFactory:
    """Factory for creating repositories."""
    
    _repositories = {}
    
    @classmethod
    def get_repository(cls, model_name: str):
        """Get repository for model."""
        if model_name not in cls._repositories:
            model_class = cls._get_model_class(model_name)
            if model_class:
                cls._repositories[model_name] = SQLAlchemyRepository(model_class)
        return cls._repositories.get(model_name)
    
    @staticmethod
    def _get_model_class(model_name: str):
        """Get model class by name."""
        models = {
            'User': User,
            'Place': Place,
            'Review': Review,
            'Amenity': Amenity
        }
        return models.get(model_name)
