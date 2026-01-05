from flask_restx import Namespace, Resource

api = Namespace("status", description="Health check")

@api.route("/")
class Status(Resource):
    def get(self):
        return {"status": "HBnB API is running"}
