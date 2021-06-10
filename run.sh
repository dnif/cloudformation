#!/bin/bash

echo "create Virtual Environment"
VIRTUAL_ENV_NAME='ve'
python3 -m venv $VIRTUAL_ENV_NAME

echo "Activate Virtual Environment"
source $VIRTUAL_ENV_NAME/bin/activate
pip3 install allure-pytest
pip3 install fabric
pip3 install fabric2
pip3 install netifaces
pip3 install requests

echo "run tests"
cd /var/tmp

#echo "executing fabfile"
#/usr/bin/python3 /opt/scripts/deployment/fabfile.py

echo "executing pytest"
pytest --alluredir=/opt/allure-results /var/tmp/test_first_time_ui_calls.py
#pytest --alluredir=/opt/allure-results /opt/test_suites/test_lc_mgmt_users_calls.py
#pytest --alluredir=/opt/allure-results /opt/test_suites/test_parser_calls.py
#pytest --alluredir=/opt/allure-results /opt/test_suites/test_dashboard_api.py
#pytest --alluredir=/opt/allure-results /opt/test_suites/test_workbook_api.py
#pytest --alluredir=/opt/allure-results /opt/test_suites/test_workbook_check.py

chmod -R 777 /opt/allure-results

echo "Deactivate Virtual Environment"
deactivate
