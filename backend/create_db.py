import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="5472",
        host="localhost",
        port="5432"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'saarthi'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute("CREATE DATABASE saarthi")
        print("Database 'saarthi' created successfully.")
    else:
        print("Database 'saarthi' already exists.")
        
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
