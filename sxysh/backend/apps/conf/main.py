# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, Blueprint
from flask.views import MethodView
import sqlite3

from ..datastore import Model, Store
from . import confBlueprint

config = None

def setup(conf):
    global config
    config = conf

class CONF(MethodView):
    def get(self):
        return jsonify(config['database'][config['store']]['tables'][config['table']])

confBlueprint.add_url_rule('/conf', view_func=CONF.as_view('conf'))