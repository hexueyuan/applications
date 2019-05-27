# -*- coding:utf-8 -*-
#!/usr/bin/env python2
import json
import os
import sys
import signal
import time

import RPi.GPIO as GPIO
import MFRC522

import sqlite3

import logger

MIFAREReader = MFRC522.MFRC522()
global_manager = {
    "conf": None,
}

def createDB(manager):
    """
    连接数据库
    """
    path = os.path.join(manager['conf'].get('database_path'), manager['conf'].get('database_name'))
    conn = sqlite3.connect(path)
    if conn is not None:
        conn.close()
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
    path = os.path.join(manager['conf'].get('database_path'), manager['conf'].get('database_name'))
    conn = sqlite3.connect(path)
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
    conn.close()

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
# 扫描标签
# =====================================================
def scanner(manager):
    conf = global_manager.get('conf')
    
    path = os.path.join(conf.get('database_path'), conf.get('database_name'))
    while True:
        try:
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            (status,uid) = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                UID = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                conn = sqlite3.connect(path)
                if conn is None:
                    logger.warning("Connect to database fail.")
                    time.sleep(1)
                    continue
                cur = conn.cursor()
                insert_sql_cmd = """
                insert into {} (TIME, ID) values({}, '{}');
                """
                insert_sql_cmd = insert_sql_cmd.format(conf.get('borrow_table'), int(time.time()), UID)
                cur.execute(insert_sql_cmd)
                conn.commit()
                conn.close()
                time.sleep(2)
        except KeyboardInterrupt:
            GPIO.cleanup()


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
    scanner(global_manager)
