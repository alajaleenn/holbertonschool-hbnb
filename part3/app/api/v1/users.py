"""
User API endpoints.
"""
from flask_restx import Namespace, Resource, fields
from app.services import shared_facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Use shared facade
facade = shared_facade

# Define user model for API documentation
user_model = api.model('User', {
    'id': fields.String(readonly=True, description='User ID'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

# Define user update model (excludes email and password)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})


@api.route('/')
class UserList(Resource):
    """User list endpoint."""
    
    @api.doc('create_user')
    @api.expect(user_model)
    @api.response(201, 'User created')
    @api.response(400, 'Email already exists')
    def post(self):
        """Create a new user (registration - public endpoint)."""
        user_data = api.payload
        
        # Check if email already exists
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        
        new_user = facade.create_user(user_data)
        return new_user.to_dict(), 201
    
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    @jwt_required()
    def get(self):
        """Get all users (requires authentication)."""
        users = facade.repository.get_all('User')
        return [user.to_dict() for user in users], 200


@api.route('/<user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    """User resource endpoint."""
    
    @api.doc('get_user')
    @api.response(200, 'Success')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get a user by ID (public endpoint)."""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200
    
    @api.doc('update_user')
    @api.expect(user_update_model)
    @api.response(200, 'User updated')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update a user (users can only update their own profile)."""
        current_user_id = get_jwt_identity()
        user_data = api.payload
        
        # Check if user exists
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # Check if user is updating their own profile
        if user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        # Prevent updating email and password through this endpoint
        if 'email' in user_data:
            return {'error': 'Email cannot be updated'}, 400
        
        if 'password' in user_data:
            return {'error': 'Password cannot be updated through this endpoint'}, 400
        
        # Prevent updating is_admin
        if 'is_admin' in user_data:
            return {'error': 'Admin status cannot be modified'}, 400
        
        # Update user (only first_name and last_name allowed)
        updated_user = facade.repository.update(user_id, 'User', user_data)
        return updated_user.to_dict(), 200