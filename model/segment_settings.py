from factory import db

# Association table for SegmentSettings and ConversationSegment
segment_settings_segment_table = db.Table('segment_settings_segment_join',
    db.Column('segment_id', db.Integer, db.ForeignKey('conversation_segment.id'), primary_key=True),
    db.Column('settings_id', db.Integer, db.ForeignKey('segment_settings.id'), primary_key=True)
)

# Association table for ModuleSetting and SegmentSettings
module_settings_join = db.Table('module_settings_join',
    db.Column('module_id', db.Integer, db.ForeignKey('module_setting.id'), primary_key=True),
    db.Column('settings_id', db.Integer, db.ForeignKey('segment_settings.id'), primary_key=True)
)

# Class table for SegmentSettings - one segment settings can be used by multiple segments
class SegmentSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    segment_id = db.Column(db.Integer, db.ForeignKey('conversation_segment.id'))  # Foreign key to ConversationSegment
    model_id = db.Column(db.Integer, db.ForeignKey('model_setting.id'))  # Foreign key to ModelSetting
    model = db.relationship('ModelSetting', back_populates='segment_settings')  # Relation to ModelSetting
    modules = db.relationship('ModuleSetting', secondary=module_settings_join, back_populates='segment_settings')  # Relation to ModuleSetting
    segments = db.relationship('ConversationSegment', secondary=segment_settings_segment_table, back_populates='settings')  # Relation to ConversationSegment

    def to_dict(self):
        """Return a dictionary representation of SegmentSettings."""
        return {
            'id': self.id,
            'model_id': self.model_id,
            'model': {
                'id': self.model.id,
                'name': self.model.model_name,
                'description': self.model.model_description
            } if self.model else None,
            'modules': get_module_options([module.id for module in self.modules])
        }

# Class table for ModelSetting table - models have a one to many relationship to SegmentSettings
class ModelSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(256))
    model_description = db.Column(db.Text)
    segment_settings = db.relationship('SegmentSettings', back_populates='model')  # Relation to SegmentSettings

# Class table for ModuleSetting table - modules have a many to many relationship to SegmentSettings
class ModuleSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(256))
    module_description = db.Column(db.Text)
    segment_settings = db.relationship('SegmentSettings', secondary=module_settings_join, back_populates='modules')  # Relation to SegmentSettings

# Function to retrieve a model by ID
def get_model_by_id(model_id):
    return ModelSetting.query.get(model_id)

# Function to retrieve a module by ID
def get_module_by_id(module_id):
    return ModuleSetting.query.get(module_id)

# Function to create a SegmentSettings instance
def create_segment_settings(settings):
    module_instances = ModuleSetting.query.filter(ModuleSetting.id.in_(settings.get('modules'))).all()
    segment_settings = SegmentSettings(
        model_id=settings.get('model_id'),
        modules=module_instances
    )
    db.session.add(segment_settings)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return segment_settings

# Function to update SegmentSettings
def update_segment_settings(segment_id, model_id, module_id):
    segment_settings = SegmentSettings.query.filter_by(id=segment_id).first()
    if segment_settings:
        segment_settings.model_id = model_id
        segment_settings.module_id = module_id
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return segment_settings
    else:
        raise ValueError("SegmentSettings not found")

#function to get segment settings in a nicely formatted way
def get_segment_settings(segment_settings_id):
    segment_settings = SegmentSettings.query.get(segment_settings_id)
    return segment_settings.to_dict() if segment_settings else None

#get all module settings and set checked to true if it is in selected_modules
def get_module_options(selected_modules):
    options = ModuleSetting.query.all()
    return [{'id': option.id, 'name': option.module_name, 'description': option.module_description, 'checked': option.id in selected_modules} for option in options]

def update_segment_settings(segment_id, model_id, modules):
    segment_settings = SegmentSettings.query.filter_by(id=segment_id).first()
    if segment_settings:
        segment_settings.model_id = model_id
        # Fetch module instances from the database
        module_instances = ModuleSetting.query.filter(ModuleSetting.id.in_(modules)).all()
        segment_settings.modules = module_instances
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return segment_settings.to_dict()
    else:
        raise ValueError("SegmentSettings not found")