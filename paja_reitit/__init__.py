# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module

db = SQLAlchemy()

from paja_reitit.util import init_colors
from paja_reitit.color.models import Color
from paja_reitit.routesetter.models import Routesetter
from paja_reitit.sector.models import Sector
from paja_reitit.route.models import Route


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    for module_name in ['route', 'color', 'routesetter', 'sector', 'dashboard']:
        module = import_module(f'paja_reitit.{module_name}.routes')
        app.register_blueprint(module.blueprint)


def configure_database(app):
    # @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

            print('> Fallback to SQLite ')
            db.create_all()
        init_colors()
            
    initialize_database()
    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()
    
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    with app.app_context():
        configure_database(app)
        register_blueprints(app)
    return app