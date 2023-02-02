from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired
from paja_reitit.sector.models import Sector

class AddSectorForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={'autofocus': True})
    
    def validate_name(form, field):
        if len(field.data) > 40:
            raise ValidationError('Name must be less than 40 characters')
        name_taken = field.data.lower() in [s.name.lower() for s in Sector.query.all()]
        if name_taken:
            raise ValidationError('Sector name is already taken')
