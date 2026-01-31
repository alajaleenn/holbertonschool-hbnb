"""
User API with admin protection.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import shared_facade
from app.utils.decorators import admin_required

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.Integer(readonly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'is_admin': fields.Boolean(),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})


@api.route('/')
class UserList(Resource):
    
    @api.doc('create_user', security='Bearer Auth')
    @api.expect(user_model)
    @jwt_required()
    @admin_required()
    def post(self):
        """Create user (Admin only)."""
        data = api.payload
        
        if shared_facade.get_user_by_email(data['email']):
            return {'error': 'Email already registered'}, 400
        
        try:
            user = shared_facade.create_user(data)
            return user.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400
    
    @api.doc('list_users', security='Bearer Auth')
    @jwt_required()
    @admin_required()
    def get(self):
        """Get all users (Admin only)."""
        users = shared_facade.get_all_users()
        return [u.to_dict() for u in users], 200


@api.route('/<int:user_id>')
class UserResource(Resource):
    
    @api.doc('get_user', security='Bearer Auth')
    @jwt_required()
    def get(self, user_id):
        """Get user by ID."""
        current_id = get_jwt_identity()
        current_user = shared_facade.get_user(current_id)
        
        user = shared_facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        if not current_user.is_admin and current_id != user_id:
            return {'error': 'Unauthorized'}, 403
        
        return user.to_dict(), 200
    
    @api.doc('update_user', security='Bearer Auth')
    @api.expect(user_model)
    @jwt_required()
    def put(self, user_id):
        """Update user."""
        current_id = get_jwt_identity()
        current_user = shared_facade.get_user(current_id)
        
        user = shared_facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        if not current_user.is_admin and current_id != user_id:
            return {'error': 'Unauthorized'}, 403
        
        data = api.payload
        
        if 'is_admin' in data and not current_user.is_admin:
            return {'error': 'Only admin can change admin status'}, 403
        
        try:
            updated = shared_facade.update_user(user_id, data)
            return updated.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
