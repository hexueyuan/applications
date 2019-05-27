from flask import Flask, request, jsonify
from flask.views import MethodView
import sqlite3

from . import config

class CURD(MethodView):
    def get(self):
        primary_keys = [x for x in config['template'] if x.get('primary-key') == True]
        sql = "SELECT * from {}".format(config['database']['table'])
        for k in primary_keys:
            if not request.args.has_key(k['prop']):
                return "Bad request", 400
            else:
                sql = sql + ' where {} = {} and'.format(k.prop, 
                    request.args[k.prop] 
                        if k.type == "number" 
                        else "'{}'".format(request.args[k.prop]))
        sql = sql[:-4] + ';'
        
        conn = sqlite3.connect(config['database']['path'])
        cursor = conn.cursor()
        cursor.execute(sql)
        rv = []
        for r in cursor.fetchall():
            item = {}
            for i in range(0, len(config['template'])):
                item[config['template'][i].prop] = r[i]
            rv.append(item)
        cursor.close()
        conn.close()
        return jsonify(rv)
    
    def post(self):
        data = request.json()
        for attr in config['template']:
            if not data.has_key(attr.prop):
                return "bad request", 400
        
        sql = "insert into {} ({}) values({});".format(config['database']['table'],
                                                        str(data.keys()).replace("'", '').strip('[]'),
                                                        str(data.values()).strip('[]'))
        conn = sqlite3.connect(config['database']['path'])
        cursor = conn.cursor()
        cursor.execute(sql)
        if cursor.rowcount != 0:
            return "OK", 200
        else:
            return "server error", 500

    def put(self):
        data = request.json()
        primary_keys = [x for x in config['template'] if x.get('primary-key') == True]
        for attr in config['template']:
            if not data.has_key(attr.prop):
                return "bad request", 400
        
        sql = "insert into {} ({}) values({});".format(config['database']['table'],
                                                        str(data.keys()).replace("'", '').strip('[]'),
                                                        str(data.values()).strip('[]'))
        conn = sqlite3.connect(config['database']['path'])
        cursor = conn.cursor()
        cursor.execute(sql)
        if cursor.rowcount != 0:
            return "OK", 200
        else:
            return "server error", 500

    def delete(self):
        primary_keys = [x for x in config['template'] if x.get('primary-key') == True]
        sql = "delete from {} where".format(config['database']['table'])
        for k in primary_keys:
            if not request.args.has_key(k['prop']):
                return "Bad request", 400
            else:
                sql = sql + ' where {} = {} and'.format(k.prop, 
                    request.args[k.prop] 
                        if k.type == "number" 
                        else "'{}'".format(request.args[k.prop]))
        sql = sql[:-4] + ';'
        conn = sqlite3.connect(config['database']['path'])
        cursor = conn.cursor()
        cursor.execute(sql)
        if cursor.rowcount != 0:
            return "OK", 200
        else:
            return "server error", 500
