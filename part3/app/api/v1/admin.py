"""
Admin-only endpoints.
"""
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.services import shared_facade
from app.utils.decorators import admin_required

api = Namespace('admin', description='Admin operations')


@api.route('/stats')
class AdminStats(Resource):
    
    @api.doc('get_stats', security='Bearer Auth')
    @jwt_required()
    @admin_required()
    def get(self):
        """Get system statistics (Admin only)."""
        users = shared_facade.get_all_users()
        places = shared_facade.get_all_places()
        reviews = shared_facade.get_all_reviews()
        amenities = shared_facade.get_all_amenities()
        
        return {
            'total_users': len(users),
            'total_places': len(places),
            'total_reviews': len(reviews),
            'total_amenities': len(amenities),
            'admin_users': len([u for u in users if u.is_admin])
        }, 200


@api.route('/users/<int:user_id>/toggle-admin')
class ToggleAdmin(Resource):
    
    @api.doc('toggle_admin', security='Bearer Auth')
    @jwt_required()
    @admin_required()
    def put(self, user_id):
        """Toggle admin status (Admin only)."""
        user = shared_facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        user.is_admin = not user.is_admin
        updated = shared_facade.update_user(user_id, {'is_admin': user.is_admin})
        
        return {
            'message': f'Admin status {"granted" if user.is_admin else "revoked"}',
            'user': updated.to_dict()
        }, 200
