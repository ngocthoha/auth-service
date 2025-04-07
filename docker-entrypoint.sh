#!/bin/sh
set -e

# Set Python path to include the current directory
export PYTHONPATH=$PYTHONPATH:/app

# Wait for the database to be ready
echo "Waiting for database to be ready..."
python -c "
import time
import sys
import psycopg2

host = '$POSTGRES_SERVER'
port = 5432
max_tries = 30
tries = 0

while tries < max_tries:
    try:
        print(f'Trying to connect to PostgreSQL database (try {tries+1}/{max_tries})...')
        conn = psycopg2.connect(
            dbname='$POSTGRES_DB',
            user='$POSTGRES_USER',
            password='$POSTGRES_PASSWORD',
            host='$POSTGRES_SERVER',
            port=5432
        )
        conn.close()
        print('PostgreSQL database is ready!')
        break
    except psycopg2.OperationalError:
        tries += 1
        print('PostgreSQL database is not ready yet, waiting...')
        time.sleep(2)
else:
    print('Could not connect to PostgreSQL database after multiple tries')
    sys.exit(1)
"

# Initialize the database
echo "Initializing database..."
cd /app
python -m app.db.init_db

# Initialize the admin user
echo "Initializing admin user..."
python /app/init_admin.py

# Start the application
echo "Starting the application..."
exec "$@" 