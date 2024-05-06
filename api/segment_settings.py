from flask_restx import Resource
from . import api
from model.segment_settings import (
    get_segment_settings
)

@api.route('/get_segment_settings/<int:id>', methods=['GET'])
class GetSegmentSettings(Resource):
    def get(self, id):
        return get_segment_settings(id)