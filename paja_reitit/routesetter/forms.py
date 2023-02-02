from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired
from paja_reitit.routesetter.models import Routesetter

class AddRoutesetterForm(FlaskForm):
    name = StringField(validators=[DataRequired()], render_kw={'autofocus': True})
    
    def validate_name(form, field):
        if len(field.data) > 40:
            raise ValidationError('Name must be less than 40 characters')
        name_taken = field.data.lower() in [rs.name.lower() for rs in Routesetter.query.all()]
        if name_taken:
            raise ValidationError('Name is already taken')
