#!/bin/bash

echo "Attivazione del venv già fatto in precedenza"

DB_FILE="db.sqlite3"
APPS=("users" "giorni_presenze" "partecipanti" "presenze")

echo "⚠️ Attenzione!! Questo cancellerà il DB e tutte le migrazioni locali."
read -p "Vuoi continuare? (y/n) " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo "Annullato."
    exit 0
fi

# 1️⃣ Cancella DB
if [ -f "$DB_FILE" ]; then
    rm "$DB_FILE"
    echo "Database cancellato."
fi

# 2️⃣ Cancella migrazioni
for app in "${APPS[@]}"; do
    MIGRATION_DIR="$app/migrations"
    if [ -d "$MIGRATION_DIR" ]; then
        find "$MIGRATION_DIR" -type f ! -name "__init__.py" -delete
        echo "Migrazioni pulite per $app"
    fi
done

# 3️⃣ Ricrea migrazioni IN ORDINE
python manage.py makemigrations users
python manage.py makemigrations giorni_presenze
python manage.py makemigrations partecipanti
python manage.py makemigrations presenze

# 4️⃣ Applica
python manage.py migrate

echo "✅ DB resettato e migrazioni applicate."