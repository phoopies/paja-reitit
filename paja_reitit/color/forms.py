from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.widgets import ColorInput
from wtforms.validators import DataRequired
from paja_reitit.color.models import Color
from paja_reitit.color.util import is_valid_hex

class ColorField(StringField):
    widget = ColorInput()

class AddColorForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={'autofocus': True})
    code = ColorField(validators=[])
    
    def validate_name(form, field):
        if len(field.data) > 40:
            raise ValidationError('Name must be less than 40 characters')
        name_taken = field.data.lower() in [c.name.lower() for c in Color.query.all()]
        if name_taken:
            raise ValidationError('Name is already taken')
    
    def validate_code(form, field):
        if field.data and not is_valid_hex(field.data):
          raise ValidationError('Color hex code is invalid')
