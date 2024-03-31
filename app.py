from flask import Flask, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_cors import CORS
from flask_jwt_extended import JWTManager
from api import api_blueprint

app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)

app.register_blueprint(api_blueprint, url_prefix='/api')
api_blueprint = Blueprint('api', __name__)

app.config['JWT_SECRET_KEY'] = 'not_so_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wingspan:I760ZgfBtz0j@localhost/wingspan'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    players = db.relationship('Player', backref='game', lazy=True)
    bird_feeder = db.relationship('Food', secondary=bird_feeder_association, backref=db.backref('games', lazy=True))
    game_deck = db.relationship('DeckCard', secondary=game_deck_association, backref=db.backref('games', lazy=True))
    discard_cards = db.relationship('DeckCard', secondary=discard_cards_association, backref=db.backref('games', lazy=True))

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

class DeckCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    points = db.Column(db.Integer)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = name = db.Column(db.String(128))

# Association table for the many-to-many relationship
bird_feeder_association = db.Table('bird_feeder',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id'), primary_key=True)
)

game_deck_association = db.Table('game_deck',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('deck_card_id', db.Integer, db.ForeignKey('deck_card.id'), primary_key=True)
)

discard_cards_association = db.Table('discard_cards',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('deck_card_id', db.Integer, db.ForeignKey('deck_card.id'), primary_key=True)
)

@app.route('/')
def hello():
    return "Hello, World!"

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)