from flask import Blueprint
from flask_restx import Api, Resource

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, title='Wingspan API', version='1.0', description='Wingspan API')
ns = api.namespace('api', description='API namespace')

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'from blueprint!'}