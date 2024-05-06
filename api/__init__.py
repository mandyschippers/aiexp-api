from flask import Blueprint
from flask_restx import Api

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, title='AIExp API', version='1.0', description='AIExp API')

from .resources import *  
from .conversation import *
from .segment_settings import *
