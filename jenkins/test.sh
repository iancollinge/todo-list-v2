#!/bin/bash

echo "Test stage"

# venv created, sourced
python3 -m venv venv
source venv/bin/activate

# install pip dependencies
pip3 install pytest flask_testing
pip3 install -r frontend/requirements.txt
pip3 install -r backend/requirements.txt

mkdir test_reports

# run pytest frontend
python3 -m pytest frontend \
    --cov=frontend/application \
    --cov-report term-missing \
    --cov-report xml:test_reports/frontend_coverage.xml \
    --junitxml=test_reports/frontend_junit_report.xml

# run pytest backend
python3 -m pytest backend \
    --cov=backend/application \
    --cov-report term-missing \
    --cov-report xml:test_reports/backend_coverage.xml \
    --junitxml=test_reports/backend_junit_report.xml

# remove venv
deactivate
rm -rf venv
