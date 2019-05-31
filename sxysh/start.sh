#!/bin/bash

PWD=$(pwd)

cd ${PWD}/backend
python main.py ../conf/application.cfg &

cd ${PWD}/frontend
npm run dev &