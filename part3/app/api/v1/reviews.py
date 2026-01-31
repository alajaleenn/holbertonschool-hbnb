"""
Review API with admin bypass.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import shared_facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'id': fields.Integer(readonly=True),
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'place_id': fields.Integer(required=True),
    'user_id': fields.Integer(required=True)
})


@api.route('/')
class ReviewList(Resource):
    
    @api.doc('create_review', security='Bearer Auth')
    @api.expect(review_model)
    @jwt_required()
    def post(self):
        """Create review."""
        data = api.payload
        
        place = shared_facade.get_place(data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404
        
        try:
            review = shared_facade.create_review(data)
            return review.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400
    
    @api.doc('list_reviews')
    def get(self):
        """Get all reviews."""
        reviews = shared_facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200


@api.route('/<int:review_id>')
class ReviewResource(Resource):
    
    @api.doc('get_review')
    def get(self, review_id):
        """Get review by ID."""
        review = shared_facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200
    
    @api.doc('update_review', security='Bearer Auth')
    @api.expect(review_model)
    @jwt_required()
    def put(self, review_id):
        """Update review."""
        current_id = get_jwt_identity()
        current_user = shared_facade.get_user(current_id)
        
        review = shared_facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        if not current_user.is_admin and review.user_id != current_id:
            return {'error': 'Unauthorized'}, 403
        
        try:
            updated = shared_facade.update_review(review_id, api.payload)
            return updated.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
    
    @api.doc('delete_review', security='Bearer Auth')
    @jwt_required()
    def delete(self, review_id):
        """Delete review (Admin can delete any)."""
        current_id = get_jwt_identity()
        current_user = shared_facade.get_user(current_id)
        
        review = shared_facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Admin bypass
        if not current_user.is_admin and review.user_id != current_id:
            return {'error': 'Unauthorized'}, 403
        
        shared_facade.delete_review(review_id)
        return {'message': 'Review deleted'}, 200
