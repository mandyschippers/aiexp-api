from flask import request
from flask_restx import Resource
from . import api
from models import Conversation, create_conversation, get_conversations

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'from blueprint!'}


@api.route('/get_conversations', methods=['GET'])
class GetConversations(Resource):
    def get(self):
        conversations = get_conversations()
        return [{'id': conversation.id, 'name': conversation.name} for conversation in conversations]

@api.route('/get_conversation/<int:id>', methods=['GET'])
class GetConversation(Resource):
    def get(self, id):
        conversation = Conversation.query.get(id)
        return {'id': conversation.id, 'name': conversation.name, 'created_date': conversation.created_date.isoformat()}

@api.route('/new_conversation', methods=['POST'])
class NewConversation(Resource):
    def post(self):
        try:
            data = request.get_json()
            conversation = create_conversation(data.get('name', ''))
            return {'conversation_id': conversation.id}
        except Exception as e:
            return {'error': str(e)}
    
        
@api.route('/message', methods=['POST'])
class GetMessage(Resource):
    def post(self):
        data = request.get_json()
        #now we can add conversation logic with langchain and llm API
        return {'received message': data.get('message', 'no message was provided')}