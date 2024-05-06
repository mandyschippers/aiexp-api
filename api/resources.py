from flask_restx import Resource
from . import api

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'from blueprint!'}