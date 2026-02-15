"""
Authentication endpoints.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import shared_facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    """User login endpoint."""
    
    @api.doc('login')
    @api.expect(login_model)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return JWT token."""
        data = api.payload
        
        # Authenticate user
        user = shared_facade.get_user_by_email(data['email'])
        
        if not user or not user.verify_password(data['password']):
            return {'error': 'Invalid credentials'}, 401
        
        # Create JWT token with is_admin claim
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'is_admin': user.is_admin}  # ← ADD THIS
        )
        
        return {
            'access_token': access_token,
            'user': user.to_dict()
        }, 200