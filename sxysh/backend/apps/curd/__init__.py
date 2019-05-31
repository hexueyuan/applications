from flask import Blueprint

curdBlueprint = Blueprint('curd', __name__)
from . import main

def setup(conf):
    main.setup(conf)

__all__ = ['setup', 'curd', 'config']