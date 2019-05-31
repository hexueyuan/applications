from apps import create_app, databaseSetup

import json
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "No configuration file."
        exit()
    if not os.path.exists(sys.argv[1]):
        print "{}: No such file!".format(sys.argv[1])
        exit()

    conf = json.load(open(sys.argv[1], 'r'))
    databaseSetup(conf['database'])

    app = create_app(__name__, conf)
    app.run(port=5051)