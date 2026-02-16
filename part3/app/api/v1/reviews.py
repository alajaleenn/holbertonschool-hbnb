"""
Review API endpoints.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import shared_facade

api = Namespace('reviews', description='Review operations')
facade = shared_facade

# Define review model for API documentation
review_model = api.model('Review', {
    'id': fields.String(readonly=True, description='Review ID'),
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID'),
    'user_id': fields.String(readonly=True, description='User ID'),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

# Define review update model (only text and rating can be updated)
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)')
})


@api.route('/')
class ReviewList(Resource):
    """Review list endpoint."""
    
    @api.doc('create_review')
    @api.expect(review_model)
    @api.response(201, 'Review created')
    @api.response(400, 'Validation error')
    @jwt_required()
    def post(self):
        """Create a new review (requires authentication)."""
        current_user_id = get_jwt_identity()
        review_data = api.payload
        
        # Automatically set user_id from token
        review_data['user_id'] = current_user_id
        
        # Validate rating
        if review_data.get('rating') and not (1 <= review_data['rating'] <= 5):
            return {'error': 'Rating must be between 1 and 5'}, 400
        
        # Check if place exists
        place = facade.get_place(review_data.get('place_id'))
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Business rule: Cannot review own place
        if place.owner_id == current_user_id:
            return {'error': 'You cannot review your own place'}, 400
        
        # Business rule: Cannot review same place twice
        existing_reviews = facade.get_reviews_by_place(review_data['place_id'])
        if not isinstance(existing_reviews, list):
            existing_reviews = [existing_reviews] if existing_reviews else []
            
        for review in existing_reviews:
            if review.user_id == current_user_id:
                return {'error': 'You have already reviewed this place'}, 400
        
        # Create review
        new_review = facade.create_review(review_data)
        return new_review.to_dict(), 201
    
    @api.doc('list_reviews')
    def get(self):
        """Get all reviews (public endpoint)."""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200


@api.route('/<review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    """Review resource endpoint."""
    
    @api.doc('get_review')
    @api.response(200, 'Success')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get a review by ID (public endpoint)."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200
    
    @api.doc('update_review')
    @api.expect(review_update_model)
    @api.response(200, 'Review updated')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @jwt_required()
    def put(self, review_id):
        """Update a review (only review author can update)."""
        current_user_id = get_jwt_identity()
        review_data = api.payload
        
        # Check if review exists
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Check if user is the review author
        if review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        # Validate rating if provided
        if 'rating' in review_data and not (1 <= review_data['rating'] <= 5):
            return {'error': 'Rating must be between 1 and 5'}, 400
        
        # Update review
        updated_review = facade.update_review(review_id, review_data)
        return updated_review.to_dict(), 200
    
    @api.doc('delete_review')
    @api.response(200, 'Review deleted')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (only review author can delete)."""
        current_user_id = get_jwt_identity()
        
        # Check if review exists
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Check if user is the review author
        if review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        # Delete review
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200