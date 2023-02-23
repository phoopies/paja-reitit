from flask import Blueprint

blueprint = Blueprint(
    'routesetter',
    __name__,
    url_prefix='/routesetters'
)