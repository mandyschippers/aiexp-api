from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from models import Game, Player, User, DeckCard, Food

    CORS(app)
    JWTManager(app)

    from api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
