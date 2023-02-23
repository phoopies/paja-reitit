from flask import Blueprint

blueprint = Blueprint(
    'color',
    __name__,
    url_prefix='/colors'
)