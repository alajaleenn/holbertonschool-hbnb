"""
Place API endpoints.
"""
from flask_restx import Namespace, Resource, fields
from app.services import shared_facade

api = Namespace('places', description='Place operations')
facade = shared_facade

# Define place model for API documentation
place_model = api.model('Place', {
    'id': fields.String(readonly=True, description='Place ID'),
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(required=True, description='Description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(required=True, description='Owner user ID'),
    'amenities': fields.List(fields.String, description='List of amenity IDs'),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})


@api.route('/')
class PlaceList(Resource):
    """Place list endpoint."""
    
    @api.doc('create_place')
    @api.expect(place_model)
    @api.response(201, 'Place created')
    @api.response(400, 'Invalid input')
    def post(self):
        """Create a new place."""
        place_data = api.payload
        
        # Validate owner exists
        owner = facade.get_user(place_data.get('owner_id'))
        if not owner:
            return {'error': 'Owner not found'}, 400
        
        # Validate amenities if provided
        if 'amenities' in place_data and place_data['amenities']:
            for amenity_id in place_data['amenities']:
                amenity = facade.get_amenity(amenity_id)
                if not amenity:
                    return {'error': f'Amenity {amenity_id} not found'}, 400
        
        try:
            # Remove amenities from place_data temporarily
            amenities = place_data.pop('amenities', [])
            
            # Create place
            new_place = facade.create_place(place_data)
            
            # Add amenities to place
            for amenity_id in amenities:
                new_place.add_amenity(amenity_id)
            
            return new_place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
    
    @api.doc('list_places')
    @api.marshal_list_with(place_model)
    def get(self):
        """Get all places."""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200


@api.route('/<place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    """Place resource endpoint."""
    
    @api.doc('get_place')
    @api.response(200, 'Success')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get a place by ID."""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200
    
    @api.doc('update_place')
    @api.expect(place_model)
    @api.response(200, 'Place updated')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input')
    def put(self, place_id):
        """Update a place."""
        place_data = api.payload
        
        # Check if place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Validate amenities if provided
        if 'amenities' in place_data and place_data['amenities']:
            for amenity_id in place_data['amenities']:
                amenity = facade.get_amenity(amenity_id)
                if not amenity:
                    return {'error': f'Amenity {amenity_id} not found'}, 400
        
        try:
            # Handle amenities separately
            if 'amenities' in place_data:
                amenities = place_data.pop('amenities')
                place.amenities = amenities
            
            # Update place
            updated_place = facade.update_place(place_id, place_data)
            return updated_place.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
