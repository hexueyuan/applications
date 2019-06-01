#!/bin/bash

CRTPWD=$(pwd)

cd ${CRTPWD}/backend
python main.py ../conf/application.cfg &

cd ${CRTPWD}/frontend
npm run dev &