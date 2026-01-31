#!/bin/bash

echo "Attivazione del venv già fatto in precedenza"

DB_FILE="db.sqlite3"

APPS=("giorni_presenze" "partecipanti" "presenze" "users")

echo "Attenzione!! Questo cancellerà il DB e tutte le migrazioni locali."

read -p "Vuoi continuare? (y/n) " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo "Annullato."
    exit 0
fi

# 1️⃣ Cancella il DB
if [ -f $DB_FILE ]; then
    rm $DB_FILE
    echo "Database $DB_FILE cancellato."
else
    echo "Database $DB_FILE non trovato, salto."
fi

# 2️⃣ Cancella le migrazioni di tutte le app
for app in "${APPS[@]}"; do
    MIGRATION_DIR="$app/migrations"
    if [ -d "$MIGRATION_DIR" ]; then
        find $MIGRATION_DIR -type f ! -name "__init__.py" -delete
        echo "Migrazioni pulite per $app"
    fi
done

# 3️⃣ Rifai migrazioni e applicale
python manage.py makemigrations
python manage.py migrate

echo "✅ DB resettato e migrazioni applicate."