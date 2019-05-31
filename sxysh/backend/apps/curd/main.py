# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, Blueprint
from flask.views import MethodView
import sqlite3

from ..datastore import Model, Store
from . import curdBlueprint

config = None

def setup(conf):
    global config
    config = conf

class CURD(MethodView):
    def get(self):
        with Store[config.get('store')] as store:
            rv = []
            records = store.query(getattr(getattr(Model, config.get('store')), config.get('table'))).all()
            for r in records:
                rv.append({k:v for k, v in r.__dict__.items() if not k.startswith('_')})
        return jsonify(rv)
    
    def post(self):
        data = request.json
        Cls = getattr(getattr(Model, config.get('store')), config.get('table'))
        keys = [k for k in Cls.__dict__.keys() if not k.startswith('_')]

        # 判断两个列表互相包含
        if set(data.keys()) != set(keys):
            return "Bad request", 400
        
        record = Cls(**data)
        with Store[config.get('store')] as store:
            store.add(record)
            store.commit()
        return "OK", 200

    def put(self):
        data = request.json
        primary_keys = [cfg['prop'] for cfg in config['database'][config['store']]['tables'][config['table']] if cfg.get('primary_key', False)]
        if not set(primary_keys).issubset(set(data.keys())):
            return "Bad request", 400
        
        with Store[config.get('store')] as store:
            tclass = getattr(getattr(Model, config.get('store')), config.get('table'))
            condition = {k:v for k, v in data.items() if k in primary_keys}
            store.query(tclass).filter_by(**condition).update({k:v for k, v in data.items() if k not in primary_keys})
            store.commit()
        return "OK", 200

    def delete(self):
        data = request.args
        primary_keys = [cfg['prop'] for cfg in config['database'][config['store']]['tables'][config['table']] if cfg.get('primary_key', False)]
        if not set(primary_keys).issubset(set(data.keys())):
            return "Bad request", 40

        with Store[config.get('store')] as store:
            tclass = getattr(getattr(Model, config.get('store')), config.get('table'))
            condition = {k:v for k, v in data.items() if k in primary_keys}
            store.query(tclass).filter_by(**condition).delete()
            store.commit()
        return "OK", 200

curdBlueprint.add_url_rule('/curd', view_func=CURD.as_view('curd'))