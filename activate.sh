#!/bin/bash

echo "Attivazione del venv automatizzato"

source venv/bin/activate

cd todolist_key

pwd

python manage.py runserver