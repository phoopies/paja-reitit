from flask import Blueprint

blueprint = Blueprint(
    'route_blueprint',
    __name__,
    url_prefix=''
)