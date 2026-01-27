"""
Authentication endpoints.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import shared_facade

api = Namespace('auth', description='Authentication operations')

# Use shared facade
facade = shared_facade

# Define login model
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    """Login endpoint."""
    
    @api.doc('login')
    @api.expect(login_model)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return JWT token."""
        credentials = api.payload
        
        # Get user by email
        user = facade.get_user_by_email(credentials['email'])
        
        # Check if user exists and password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401
        
        # Create JWT token with user identity and role
        access_token = create_access_token(
            identity=user.id,
            additional_claims={'is_admin': user.is_admin}
        )
        
        return {
            'access_token': access_token,
            'user_id': user.id
        }, 200