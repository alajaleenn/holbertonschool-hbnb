"""
Place API endpoints.
"""
from flask_restx import Namespace, Resource, fields
from app.services import shared_facade

api = Namespace('places', description='Place operations')

# Use shared facade
facade = shared_facade

# Define place model for API documentation
place_model = api.model('Place', {
    'id': fields.String(readonly=True, description='Place ID'),
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(required=True, description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
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
    @api.response(400, 'Validation error')
    @api.response(404, 'Owner not found')
    def post(self):
        """Create a new place."""
        place_data = api.payload
        
        # Validate price (must be positive)
        if place_data['price'] <= 0:
            return {'error': 'Price must be positive'}, 400
        
        # Validate latitude (-90 to 90)
        if not -90 <= place_data['latitude'] <= 90:
            return {'error': 'Latitude must be between -90 and 90'}, 400
        
        # Validate longitude (-180 to 180)
        if not -180 <= place_data['longitude'] <= 180:
            return {'error': 'Longitude must be between -180 and 180'}, 400
        
        # Check if owner exists
        owner = facade.get_user(place_data['owner_id'])
        if not owner:
            return {'error': 'Owner not found'}, 404
        
        new_place = facade.create_place(place_data)
        return new_place.to_dict(), 201
    
    @api.doc('list_places')
    @api.marshal_list_with(place_model)
    def get(self):
        """Get all places."""
        places = facade.repository.get_all('Place')
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
    @api.response(400, 'Validation error')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Update a place."""
        place_data = api.payload
        
        # Check if place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Validate price if provided
        if 'price' in place_data and place_data['price'] <= 0:
            return {'error': 'Price must be positive'}, 400
        
        # Validate latitude if provided
        if 'latitude' in place_data and not -90 <= place_data['latitude'] <= 90:
            return {'error': 'Latitude must be between -90 and 90'}, 400
        
        # Validate longitude if provided
        if 'longitude' in place_data and not -180 <= place_data['longitude'] <= 180:
            return {'error': 'Longitude must be between -180 and 180'}, 400


        # Update place
        updated_place = facade.repository.update(place_id, 'Place', place_data)
        return updated_place.to_dict(), 200


@api.route('/<place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    """Place reviews endpoint."""

    @api.doc('get_place_reviews')
    @api.response(200, 'Success')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place."""
        # Check if place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Get all reviews for this place
        reviews = facade.get_reviews_by_place(place_id)
        return [review.to_dict() for review in reviews], 200
