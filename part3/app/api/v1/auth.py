"""
Authentication endpoints.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import shared_facade

api = Namespace('auth', description='Authentication')

login_model = api.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

register_model = api.model('Register', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})


@api.route('/register')
class Register(Resource):
    
    @api.doc('register')
    @api.expect(register_model)
    def post(self):
        """Register new user."""
        data = api.payload
        
        if shared_facade.get_user_by_email(data['email']):
            return {'error': 'Email already registered'}, 400
        
        try:
            user = shared_facade.create_user(data)
            token = create_access_token(identity=user.id)
            return {
                'access_token': token,
                'user': user.to_dict()
            }, 201
        except Exception as e:
            return {'error': str(e)}, 400


@api.route('/login')
class Login(Resource):
    
    @api.doc('login')
    @api.expect(login_model)
    def post(self):
        """User login."""
        data = api.payload
        
        user = shared_facade.authenticate_user(data['email'], data['password'])
        if not user:
            return {'error': 'Invalid credentials'}, 401
        
        token = create_access_token(identity=user.id)
        return {
            'access_token': token,
            'user': user.to_dict()
        }, 200


@api.route('/profile')
class Profile(Resource):
    
    @api.doc('profile', security='Bearer Auth')
    @jwt_required()
    def get(self):
        """Get current user profile."""
        user_id = get_jwt_identity()
        user = shared_facade.get_user(user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        return user.to_dict(), 200
