from flask import Blueprint

blueprint = Blueprint(
    'sector',
    __name__,
    url_prefix='/sectors'
)