#!/bin/bash

nohup python backend/main.py conf/config.backend.json &
nohup python scanner/main.py conf/config.scanner.json &
echo "Setup!"
