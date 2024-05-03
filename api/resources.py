from flask import request
from flask_restx import Resource
from . import api

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'from blueprint!'}
    
@api.route('/message', methods=['POST'])
class GetMessage(Resource):
    def post(self):
        data = request.get_json()
        #now we can add conversation logic with langchain and llm API
        return {'received message': data.get('message', 'no message was provided')}
