from flask import request
from flask_restx import Resource
from . import api
from models import Conversation, create_conversation

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'from blueprint!'}


@api.route('/new_conversation', methods=['POST'])
class NewConversation(Resource):
    def post(self):
        try:
            data = request.get_json()
            conversation = create_conversation(data.get('name', ''))
            return {'conversation id': conversation.id}
        except Exception as e:
            return {'error': str(e)}
    
        
@api.route('/message', methods=['POST'])
class GetMessage(Resource):
    def post(self):
        data = request.get_json()
        #now we can add conversation logic with langchain and llm API
        return {'received message': data.get('message', 'no message was provided')}