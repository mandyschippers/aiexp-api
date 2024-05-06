from flask import request
from flask_restx import Resource
from . import api
from config import Config
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from model.conversation import (
    Conversation,
    create_conversation,
    get_conversations,
    create_segment,
    update_segment_reply

)

# API routes related to conversations

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
class Message(Resource):
    def post(self):
        data = request.get_json()
        conversation_id = data.get('conversation_id')
        message = data.get('message')
        message_history = data.get('message_history')
        #assemble chat history from segments
        history = create_chain_from_segments(message_history, message)
        #create the next segment in the conversation
        segment = create_segment(conversation_id, message)
        #call the LLM
        llm = ChatOpenAI(api_key=Config.OPENAI_API_KEY)
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Answer all questions to the best of your ability.",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        chain = prompt | llm
        response = chain.invoke(
            {
                "messages": history.messages,
            }
        )
        #save response.content to the segment
        update_segment_reply(segment.id, response.content)
        return {'received message': data.get('message', 'no message was provided') + 'with reply: ' + response.content + 'from segment ' + str(segment.id) + ' in conversation ' + str(conversation_id)}

@api.route('/get_segments/<int:id>', methods=['GET'])
class GetSegments(Resource):
    def get(self, id):
        conversation = Conversation.query.get(id)
        segments = conversation.segments
        return [{'id': segment.id, 'message': segment.message, 'reply': segment.reply} for segment in segments]
    
def create_chain_from_segments(segments, message):
    history = ChatMessageHistory()
    if segments:
        for segment in segments:
            history.add_user_message(segment['message'])
            #add ai message of reply if exists or else an empty string in one line
            if segment['reply']:
                history.add_ai_message(segment['reply'])
    history.add_user_message(message)
    return history