from apps import create_app

import json
import sys
import os

def usage():
    print "python main.py <config-file>"

def getConf(path):
    with open(path, 'r') as f:
        return json.load(f)

def argvCheck():
    if len(sys.argv) != 2:
        usage()
        exit()
    if not os.path.exists(sys.argv[1]):
        print "{}: No such file!".format(sys.argv[1])
        exit()

def convertInitDB(conf):
    # a table
    sql = "create table if not exists {} ();".format(conf['database']['table'])
    cols = ""

if __name__ == "__main__":
    argvCheck()
    conf = getConf(sys.argv[1])

    app = create_app(__name__)
    host = conf
    app.run()