"""
Place API endpoints.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import shared_facade

api = Namespace('places', description='Place operations')
facade = shared_facade

place_model = api.model('Place', {
    'id': fields.String(readonly=True, description='Place ID'),
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(required=True, description='Description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(readonly=True, description='Owner ID'),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})


@api.route('/')
class PlaceList(Resource):
    """Place list endpoint."""
    
    @api.doc('create_place')
    @api.expect(place_model)
    @api.response(201, 'Place created')
    @api.response(400, 'Validation error')
    @jwt_required()
    def post(self):
        """Create a new place (requires authentication)."""
        current_user_id = get_jwt_identity()
        place_data = api.payload
        
        # Automatically set owner_id from token
        place_data['owner_id'] = current_user_id
        
        # Validate price
        if place_data.get('price') and place_data['price'] <= 0:
            return {'error': 'Price must be positive'}, 400
        
        # Validate coordinates
        if place_data.get('latitude') and not (-90 <= place_data['latitude'] <= 90):
            return {'error': 'Invalid latitude'}, 400
        
        if place_data.get('longitude') and not (-180 <= place_data['longitude'] <= 180):
            return {'error': 'Invalid longitude'}, 400
        
        # Create place
        new_place = facade.create_place(place_data)
        return new_place.to_dict(), 201
    
    @api.doc('list_places')
    def get(self):
        """Get all places (public endpoint)."""
        places = facade.get_all_places()
        return [p.to_dict() for p in places], 200


@api.route('/<place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    """Place resource endpoint."""
    
    @api.doc('get_place')
    @api.response(200, 'Success')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get a place by ID (public endpoint)."""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200
    
    @api.doc('update_place')
    @api.expect(place_model)
    @api.response(200, 'Place updated')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        """Update a place (only owner can update)."""
        current_user_id = get_jwt_identity()
        place_data = api.payload
        
        # Check if place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Check if user is the owner
        if place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        # Validate price if provided
        if 'price' in place_data and place_data['price'] <= 0:
            return {'error': 'Price must be positive'}, 400
        
        # Validate coordinates if provided
        if 'latitude' in place_data and not (-90 <= place_data['latitude'] <= 90):
            return {'error': 'Invalid latitude'}, 400
        
        if 'longitude' in place_data and not (-180 <= place_data['longitude'] <= 180):
            return {'error': 'Invalid longitude'}, 400
        
        # Update place
        updated_place = facade.update_place(place_id, place_data)
        return updated_place.to_dict(), 200