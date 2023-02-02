"""
Classes for listings
"""

from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import optional
from paja_reitit.color.models import Color
from paja_reitit.routesetter.models import Routesetter
from paja_reitit.sector.models import Sector
from paja_reitit.util import GRADES

class CreateRouteForm(FlaskForm):

    setter       = SelectField(validators=[optional()], choices=[], render_kw={'autofocus': True})    
    grade        = SelectField(validators=[optional()], choices=GRADES)
    color        = SelectField(validators=[optional()], choices=[])
    sector       = SelectField(validators=[optional()], choices=[])

    def __init__(self, formdata=None, **kwargs):
        super().__init__(formdata, **kwargs)
        setters = sorted(Routesetter.query.all(), key=lambda rs: -1*rs.routes_set)
        self.setter.choices = [(rs.id, rs.name) for rs in setters]
        self.setter.choices.insert(0, (None, "Anonymous"))
        
        self.color.choices  = [(c.id, c.name) for c in Color.query.all()]
        
        self.sector.choices = [(s.id, s.name) for s in Sector.query.all()]
        
        for choices in [self.color.choices, self.sector.choices]:
            choices.insert(0, (None, "Unknown"))