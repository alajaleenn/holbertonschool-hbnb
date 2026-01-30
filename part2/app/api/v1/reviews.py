"""
Review API endpoints.
"""
from flask_restx import Namespace, Resource, fields
from app.services import shared_facade

api = Namespace('reviews', description='Review operations')

# Initialize facade
facade = shared_facade

# Define review model for API documentation
review_model = api.model('Review', {
    'id': fields.String(readonly=True, description='Review ID'),
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID'),
    'user_id': fields.String(required=True, description='User ID'),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})


@api.route('/')
class ReviewList(Resource):
    """Review list endpoint."""
    
    @api.doc('create_review')
    @api.expect(review_model)
    @api.response(201, 'Review created')
    @api.response(400, 'Validation error')
    @api.response(404, 'Place or User not found')
    def post(self):
        """Create a new review."""
        review_data = api.payload
        
        # Validate rating (1-5)
        if not 1 <= review_data['rating'] <= 5:
            return {'error': 'Rating must be between 1 and 5'}, 400
        
        # Check if place exists
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Check if user exists
        user = facade.get_user(review_data['user_id'])
        if not user:
            return {'error': 'User not found'}, 404
        
        # Check if user is trying to review their own place
        if place.owner_id == review_data['user_id']:
            return {'error': 'You cannot review your own place'}, 400
        
        # Create review
        try:
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
    
    @api.doc('list_reviews')
    @api.marshal_list_with(review_model)
    def get(self):
        """Get all reviews."""
        reviews =
