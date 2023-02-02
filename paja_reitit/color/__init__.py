from flask import Blueprint

blueprint = Blueprint(
    'color_blueprint',
    __name__,
    url_prefix='/colors'
)