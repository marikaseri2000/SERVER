#!/bin/bash

echo "Attivazione del venv automatizzato"

source venv/bin/activate

cd todolist_key

# Verifica che sia passato un nome
if [ -z "$1" ]; then
  echo "Uso: ./startapp.sh nome_app"
  exit 1
fi

APP_NAME=$1
SETTINGS_FILE="todolist_key/settings.py" 

# Crea l'app Django
python manage.py startapp $APP_NAME
echo "App '$APP_NAME' creata."

# Chiedi se aggiungere automaticamente a INSTALLED_APPS
read -p "Vuoi aggiungere $APP_NAME a INSTALLED_APPS? (y/n) " yn
case $yn in
    [Yy]* )
        sed -i "/INSTALLED_APPS = \[/a \    '$APP_NAME'," $SETTINGS_FILE
        echo "$APP_NAME aggiunta a INSTALLED_APPS."
        ;;
    * ) echo "Non aggiunta a INSTALLED_APPS.";;
esac