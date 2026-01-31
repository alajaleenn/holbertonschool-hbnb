"""
Amenity API with admin protection.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.services import shared_facade
from app.utils.decorators import admin_required

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True)
})


@api.route('/')
class AmenityList(Resource):
    
    @api.doc('create_amenity', security='Bearer Auth')
    @api.expect(amenity_model)
    @jwt_required()
    @admin_required()
    def post(self):
        """Create amenity (Admin only)."""
        try:
            amenity = shared_facade.create_amenity(api.payload)
            return amenity.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400
    
    @api.doc('list_amenities')
    def get(self):
        """Get all amenities."""
        amenities = shared_facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200


@api.route('/<int:amenity_id>')
class AmenityResource(Resource):
    
    @api.doc('get_amenity')
    def get(self, amenity_id):
        """Get amenity by ID."""
        amenity = shared_facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200
    
    @api.doc('update_amenity', security='Bearer Auth')
    @api.expect(amenity_model)
    @jwt_required()
    @admin_required()
    def put(self, amenity_id):
        """Update amenity (Admin only)."""
        amenity = shared_facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        try:
            updated = shared_facade.update_amenity(amenity_id, api.payload)
            return updated.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
