from flask import Flask

__all__ = ['create_app', 'config']
config = None

def create_app(name, conf):
    app = Flask(name)
    config = conf

    # add blueprint
    # ......

    return app