from flask import Blueprint

confBlueprint = Blueprint('conf', __name__)
from . import main

def setup(conf):
    main.setup(conf)

__all__ = ['setup', 'confBlueprint']