from flask import Flask, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy

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

db = SQLAlchemy(app)

@app.route('/')
def hello():
    return "Hello, World!"

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)