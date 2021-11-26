#!/bin/bash

echo "Test stage"

# venv created, sourced
python3 -m venv venv
source venv/bin/activate

# install pip dependencies
pip3 install pytest flask_testing
pip3 install -r frontend/requirements.txt
pip3 install -r backend/requirements.txt

# run pytest frontend
python3 -m pytest frontend 

# run pytest backend
python3 -m pytest backend

# remove venv
deactivate
rm -rf venv
