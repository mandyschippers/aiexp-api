from flask import Blueprint
from flask_restx import Api

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, title='Wingspan API', version='1.0', description='Wingspan API')

from .resources import *  
