"""
User API endpoints.
"""
from flask_restx import Namespace, Resource, fields
from app.services import shared_facade

api = Namespace('users', description='User operations')

# Use shared facade
facade = shared_facade

# Define user model for API documentation
user_model = api.model('User', {
    'id': fields.String(readonly=True, description='User ID'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})


@api.route('/')
class UserList(Resource):
    """User list endpoint."""
    
    @api.doc('create_user')
    @api.expect(user_model)
    @api.response(201, 'User created')
    @api.response(400, 'Email already exists')
    def post(self):
        """Create a new user."""
        user_data = api.payload
        
        # Check if email already exists
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        
        new_user = facade.create_user(user_data)
        return new_user.to_dict(), 201
    
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """Get all users."""
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
        """Get a user by ID."""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200
    
    @api.doc('update_user')
    @api.expect(user_model)
    @api.response(200, 'User updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Email already registered')
    def put(self, user_id):
        """Update a user."""
        user_data = api.payload
        
        # Check if user exists
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # If email is being changed, check if new email already exists
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400
        
        # Update user
        updated_user = facade.repository.update(user_id, 'User', user_data)
        return updated_user.to_dict(), 200
