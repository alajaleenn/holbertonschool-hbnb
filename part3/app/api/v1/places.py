"""
Place API with admin bypass.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import shared_facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'id': fields.Integer(readonly=True),
    'title': fields.String(required=True),
    'description': fields.String(required=True),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.Integer(required=True)
})


@api.route('/')
class PlaceList(Resource):
    
    @api.doc('create_place', security='Bearer Auth')
    @api.expect(place_model)
    @jwt_required()
    def post(self):
        """Create place."""
        data = api.payload
        
        owner = shared_facade.get_user(data['owner_id'])
        if not owner:
            return {'error': 'Owner not found'}, 400
        
        try:
            place = shared_facade.create_place(data)
            return place.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400
    
    @api.doc('list_places')
    def get(self):
        """Get all places."""
        places = shared_facade.get_all_places()
        return [p.to_dict() for p in places], 200


@api.route('/<int:place_id>')
class PlaceResource(Resource):
    
    @api.doc('get_place')
    def get(self, place_id):
        """Get place by ID."""
        place = shared_facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200
    
    @api.doc('update_place', security='Bearer Auth')
    @api.expect(place_model)
    @jwt_required()
    def put(self, place_id):
        """Update place (Admin can update any)."""
        current_id = get_jwt_identity()
        current_user = shared_facade.get_user(current_id)
        
        place = shared_facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Admin bypass
        if not current_user.is_admin and place.owner_id != current_id:
            return {'error': 'Unauthorized'}, 403
        
        try:
            updated = shared_facade.update_place(place_id, api.payload)
            return updated.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
