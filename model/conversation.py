from factory import db
import datetime
from model.segment_settings import SegmentSettings, create_segment_settings

# Association table for Conversation and ConversationSegment
conversation_segment_table = db.Table('conversation_segment_join',
    db.Column('conversation_id', db.Integer, db.ForeignKey('conversation.id'), primary_key=True),
    db.Column('segment_id', db.Integer, db.ForeignKey('conversation_segment.id'), primary_key=True)
)

# Class table for Conversation - a conversation is a collection of segments
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    segments = db.relationship('ConversationSegment', secondary=conversation_segment_table, back_populates='conversations')

# Class table for ConversationSegment - a segment can occur in multiple conversations
class ConversationSegment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    reply = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    conversations = db.relationship('Conversation', secondary=conversation_segment_table, back_populates='segments')
    settings_id = db.Column(db.Integer, db.ForeignKey('segment_settings.id'))
    settings = db.relationship('SegmentSettings', back_populates='segments')


#need to be able to create a new conversation in the database
def create_conversation(name):
    conversation = Conversation(name=name)
    db.session.add(conversation)
    db.session.commit()
    return conversation

#get a list of all conversations in the database
def get_conversations():
    return Conversation.query.all()

#create the next segment in a conversation with id conversation_id
def create_segment(conversation_id, message, segment_settings):
    conversation = Conversation.query.get(conversation_id)
    if conversation is None:
        raise ValueError("Conversation not found")
    
    new_segment = ConversationSegment(message=message)
    
    if segment_settings:
        settings_instance = create_segment_settings(segment_settings)
        new_segment.settings = settings_instance
        #else if conversation has at least one segment, use the settings from the last segment
    elif conversation.segments:
        last_segment = conversation.segments[-1]
        new_segment.settings = last_segment.settings
    else:
        standard_settings = get_standard_settings()
        if standard_settings is None:
            raise ValueError("Standard settings not found")
        new_segment.settings = standard_settings

    conversation.segments.append(new_segment)

    db.session.add(new_segment)
    try:
        db.session.commit()
    except Exception as e:  
        db.session.rollback()
        raise e
    
    return new_segment

def update_segment_reply(segment_id, reply):
    segment = ConversationSegment.query.get(segment_id)
    segment.reply = reply
    db.session.commit()
    return segment

def get_standard_settings():
    return SegmentSettings.query.get(1)