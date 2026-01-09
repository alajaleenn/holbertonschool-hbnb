"""
Amenity API endpoints.
"""
from flask_restx import Namespace, Resource, fields
from app.services import shared_facade

api = Namespace('amenities', description='Amenity operations')

facade = shared_facade

amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='Amenity ID'),
    'name': fields.String(required=True, description='Amenity name'),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})


@api.route('/')
class AmenityList(Resource):
    """Amenity list endpoint."""
    
    @api.doc('create_amenity')
    @api.expect(amenity_model)
    @api.response(201, 'Amenity created')
    def post(self):
        """Create a new amenity."""
        amenity_data = api.payload
        new_amenity = facade.create_amenity(amenity_data)
        return new_amenity.to_dict(), 201
    
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_model)
    def get(self):
        """Get all amenities."""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200


@api.route('/<amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    """Amenity resource endpoint."""
    
    @api.doc('get_amenity')
    @api.response(200, 'Success')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get an amenity by ID."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200
    
    @api.doc('update_amenity')
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update an amenity."""
        amenity_data = api.payload
        
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        return updated_amenity.to_dict(), 200
