from factory import db

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

hand_association = db.Table('hand',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
    db.Column('deck_card_id', db.Integer, db.ForeignKey('deck_card.id'), primary_key=True)
)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    players = db.relationship('Player', backref='game', lazy=True)
    bird_feeder = db.relationship('Food', secondary=bird_feeder_association, backref=db.backref('games', lazy=True))
    game_deck = db.relationship('DeckCard', secondary=game_deck_association, backref=db.backref('games', lazy=True))
    discard_cards = db.relationship('DeckCard', secondary=discard_cards_association, backref=db.backref('games', lazy=True))

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hand = db.relationship('DeckCard', secondary=hand_association, backref=db.backref('games', lazy=True))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    points = db.Column(db.Integer)

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
