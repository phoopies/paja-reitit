from flask import Blueprint

blueprint = Blueprint(
    'routesetter_blueprint',
    __name__,
    url_prefix='/routesetters'
)