from flask import Blueprint

blueprint = Blueprint(
    'sector_blueprint',
    __name__,
    url_prefix='/sectors'
)