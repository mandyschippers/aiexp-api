from factory import db
import datetime

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
    settings_id = db.Column(db.Integer, db.ForeignKey('segment_settings.id')) # Foreign key to SegmentSettings
    settings = db.relationship('SegmentSettings', back_populates='segments')  # Relation to SegmentSettings

# Class table for SegmentSettings - a segment has one segment settings, but a segment settings can be used by multiple segments
class SegmentSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    segments = db.relationship('ConversationSegment', back_populates='settings')  # Relation to ConversationSegment

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
def create_segment(conversation_id, message):
    print('conversation_id:', conversation_id)
    print('message:', message)
    conversation = Conversation.query.get(conversation_id)
    segment = ConversationSegment(message=message)
    conversation.segments.append(segment)
    db.session.add(segment)
    db.session.commit()
    return segment