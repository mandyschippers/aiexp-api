from flask_restx import Resource
from . import api
from model.segment_settings import (
    ModelSetting,
    ModuleSetting,
    get_segment_settings
)

@api.route('/get_segment_settings/<int:id>', methods=['GET'])
class GetSegmentSettings(Resource):
    def get(self, id):
        return get_segment_settings(id)
    
@api.route('/get_model_options', methods=['GET'])
class GetModelOptions(Resource):
    def get(self):
        options = ModelSetting.query.all()
        return [{'id': option.id, 'name': option.model_name, 'description': option.model_description} for option in options]
    
@api.route('/get_module_options', methods=['GET'])
class GetModuleOptions(Resource):
    def get(self):
        options = ModuleSetting.query.all()
        return [{'id': option.id, 'name': option.module_name, 'description': option.module_description} for option in options]