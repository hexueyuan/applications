# -*- coding:utf-8 -*-
#!/usr/bin/env python2
import json
import os
import sys
import signal
import time

import sqlite3

from flask import Flask, make_response, request, redirect

import logger

app = Flask(__name__)
root = os.path.dirname(os.path.abspath(sys.argv[0]))

global_manager = {
    "conf": None,
    "db_conn": None
}

def createDB(manager):
    """
    连接数据库
    """
    path = os.path.join(manager['conf'].get('database_path'), manager['conf'].get('database_name'))
    conn = sqlite3.connect(path)
    if conn is not None:
        manager["db_conn"] = conn
        logger.info("Connect to database successfully!")
        return True
    else:
        logger.error("COnnect to database fail!")
        return False

def createTableIfNotExist(manager):
    """
    当表不存在时创建表
    """
    conf = manager['conf']
    conn = manager['db_conn']
    try:
        book_sql_cmd = """
        create table if not exists {}
        (ID TEXT, NAME TEXT, AUTHOR TEXT, DATE TEXT);
        """.format(conf['book_table'])
        conn.execute(book_sql_cmd)
        logger.info("Create book table successfully!")
    except Exception as e:
        logger.error("Create book table fail![{}]".format(str(e)))
    try:
        borrow_sql_cmd = """
        create table if not exists {}
        (TIME INTEGER, ID TEXT);
        """.format(conf['borrow_table'])
        conn.execute(borrow_sql_cmd)
        logger.info("Create borrow table successfully!")
    except Exception as e:
        logger.error("Create borrow table fail![{}]".format(str(e)))
    conn.commit()

def load_conf(conf_path, manager):
    """
    根据配置文件路径来加载配置
    """
    with open(conf_path) as f:
        text = f.read() 
    try:
        conf = json.loads(text)
        manager['conf'] = conf
        return True
    except Exception as e:
        print "Init manager fail![{}]".format(str(e))
        return False

def init_env(manager):
    """
    初始化环境，包括连接数据库和创建表
    """
    if not createDB(manager):
        exit()
    createTableIfNotExist(manager)

def clean_env(manager):
    """
    清除环境并退出，断开数据库连接
    """
    manager['db_conn'].close()
    logger.info("Close dbtabse.")

def exithandler(signum, frame):
    """
    捕获进程退出信号后的处理函数，执行清除函数
    """
    logger.info("Ready to exit...")
    clean_env(global_manager)
    logger.info("EXIT.")
    exit()

# =====================================================
# 路由服务
# =====================================================

# ---------
# 接口
# ---------

@app.route('/api/borrow', methods = ['GET'])
def get_borrow_table():
    conf = global_manager.get('conf')
    borrows = []

    path = os.path.join(conf.get('database_path'), conf.get('database_name'))
    conn = sqlite3.connect(path)
    if conn is None:
        logger.warning("Connect to database fail.")
        return "Connect to database fail", 500

    cur = conn.cursor()
    results = cur.execute("SELECT TIME, ID from {};".format(conf['borrow_table']))
    for row in results:
        borrows.append({"time": row[0], "id": row[1]})

    for borrow in borrows:
        cur.execute("select NAME, AUTHOR, DATE from {} where ID = '{}';".format(conf['book_table'], borrow['id']))
        result = cur.fetchall() 
        if len(result) != 1:
            borrow['name'] = u'未知书籍' + borrow['id']
            borrow['author'] = u'未知书籍作者'
            borrow['date'] = u'未知书籍出版日期'
            borrow['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(borrow['time'])) 
        else:
            borrow['name'] = result[0][0]
            borrow['author'] = result[0][1]
            borrow['date'] = result[0][2]
            borrow['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(borrow['time'])) 
    conn.close()
    resp = make_response(json.dumps(borrows))
    resp.headers['content-type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/api/book', methods = ['GET'])
def get_book_table():
    books = []

    path = os.path.join(global_manager['conf'].get('database_path'), global_manager['conf'].get('database_name'))
    conn = sqlite3.connect(path)
    if conn is None:
        logger.warning("Connect to database fail.")
        return "Connect to database fail", 500

    cur = conn.cursor()
    results = cur.execute("SELECT ID, NAME, AUTHOR, DATE from books")
    for row in results:
        books.append({"id": row[0], "name": row[1], "author": row[2], "date": row[3]})
    conn.close()
    resp = make_response(json.dumps(books))
    resp.headers['content-type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/api/book', methods = ['POST'])
def post_book_table():
    conf = global_manager['conf']
    book = request.form

    path = os.path.join(global_manager['conf'].get('database_path'), global_manager['conf'].get('database_name'))
    conn = sqlite3.connect(path)
    if conn is None:
        logger.warning("Connect to database fail.")
        return "Connect to database fail", 500
    cur = conn.cursor()

    insert_sql_cmd = u"""
    insert into {} (ID, NAME, AUTHOR, DATE) values ('{}', '{}', '{}', '{}');
    """.format(conf.get('book_table'), book['id'], book['name'], book['author'], book['date'])
    logger.debug(insert_sql_cmd)
    cur.execute(insert_sql_cmd)
    conn.commit()
    conn.close()
    resp = make_response(json.dumps({"status": "success", "errMsg": ""}))
    resp.headers['content-type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/api/book', methods = ['PUT'])
def put_book_table():
    conf = global_manager['conf']
    book = request.form

    path = os.path.join(global_manager['conf'].get('database_path'), global_manager['conf'].get('database_name'))
    conn = sqlite3.connect(path)
    if conn is None:
        logger.warning("Connect to database fail.")
        return "Connect to database fail", 500
    cur = conn.cursor()

    update_sql_cmd = u"""
    update {} set NAME = '{}', AUTHOR = '{}', DATE = '{}' WHERE ID = '{}';
    """.format(conf.get('book_table'), book['name'], book['author'], book['date'], book['id'])
    logger.debug(update_sql_cmd)
    cur.execute(update_sql_cmd)
    conn.commit()
    conn.close()
    resp = make_response(json.dumps({"status": "success", "errMsg": ""}))
    resp.headers['content-type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/api/book', methods = ['DELETE'])
def delete_book_table():
    conf = global_manager['conf']
    book = json.loads(request.data)

    path = os.path.join(global_manager['conf'].get('database_path'), global_manager['conf'].get('database_name'))
    conn = sqlite3.connect(path)
    if conn is None:
        logger.warning("Connect to database fail.")
        return "Connect to database fail", 500
    cur = conn.cursor()
    
    delete_sql_cmd = u"""
    delete from {} WHERE ID = '{}';
    """.format(conf.get('book_table'), book['id'])
    logger.debug(delete_sql_cmd)
    cur.execute(delete_sql_cmd)
    conn.commit()
    conn.close()
    resp = make_response(json.dumps({"status": "success", "errMsg": ""}))
    resp.headers['content-type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

# --------
# server
# --------
@app.route('/index.html')
def index():
    with open(os.path.join(root, 'dist/index.html')) as f:
        return f.read()

@app.route('/')
def default():
    return redirect('/index.html')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "\033[31mNo configuration file specified.\033[0m"
        print "\nUsage: \n\tpython main.py <conf_file_path>"
        print "..."
        exit()
    if not os.path.isfile(sys.argv[1]):
        print "\033[31m{}: No such configure file!\033[0m".format(sys.argv[1])
        print "\nUsage: \n\tpython main.py <conf_file_path>"
        print "..."
        exit()
    if not load_conf(sys.argv[1], global_manager):
        print "\033[31mBad config fail, some syntax error in it.\033[0m"
        exit()
    logger.config(global_manager['conf'])
    logger.info("LOG initialized!")
    signal.signal(signal.SIGINT, exithandler)
    signal.signal(signal.SIGQUIT, exithandler)

    init_env(global_manager)
    app.run(host='0.0.0.0', port=80)
