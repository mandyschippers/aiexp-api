from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'not_so_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wingspan:I760ZgfBtz0j@localhost/wingspan'
db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)

@app.route('/')
def hello():
    return "Hello, World!"

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)