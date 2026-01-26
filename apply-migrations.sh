#!/bin/bash

echo "Attivazione del venv automatizzato"

source venv/bin/activate

echo "Entro nella cartella su cui stiamo lavorando"

cd todolist_key

python manage.py makemigrations

echo"Migrazioni create, inizio a migrare"

python manage.py migrate

python manage.py runserver