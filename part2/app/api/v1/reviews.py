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
        
        # Create review
        new_review = facade.create_review(review_data)
        return new_review.to_dict(), 201
    
    @api.doc('list_reviews')
    @api.marshal_list_with(review_model)
    def get(self):
        """Get all reviews."""
        reviews = facade.repository.get_all('Review')
        return [review.to_dict() for review in reviews], 200


@api.route('/<review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    """Review resource endpoint."""
    
    @api.doc('get_review')
    @api.response(200, 'Success')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get a review by ID."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200
    
    @api.doc('update_review')
    @api.expect(review_model)
    @api.response(200, 'Review updated')
    @api.response(400, 'Validation error')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review."""
        review_data = api.payload
        
        # Check if review exists
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Validate rating if provided
        if 'rating' in review_data and not 1 <= review_data['rating'] <= 5:
            return {'error': 'Rating must be between 1 and 5'}, 400
        
        # Update review
        updated_review = facade.repository.update(review_id, 'Review', review_data)
        return updated_review.to_dict(), 200
    
    @api.doc('delete_review')
    @api.response(204, 'Review deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Delete review
        facade.delete_review(review_id)
        return '', 204
