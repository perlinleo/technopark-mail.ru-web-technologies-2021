#!/bin/bash
python3 -m venv venv
cd venv
source bin/activate
cd .. 
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py filldatabase --full 10
python3 manage.py runserver