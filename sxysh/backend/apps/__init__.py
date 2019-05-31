from flask import Flask
from .datastore import setup as databaseSetup
from .curd import curdBlueprint, setup as curdSetup
from .conf import confBlueprint, setup as confSetup

__all__ = ['create_app', 'databaseSetup']

def create_app(name, conf):
    app = Flask(name)
    curdSetup(conf)
    confSetup(conf)

    app.register_blueprint(curdBlueprint)
    app.register_blueprint(confBlueprint)

    return app