import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import sys
import getpass

# Configuration
DB_NAME = "kabarak_lost_found"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"

# Determine paths relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_FILE = os.path.join(SCRIPT_DIR, "schema.sql")
SEED_FILE = os.path.join(SCRIPT_DIR, "seed.sql")

def get_connection(dbname=None, user=None, password=None):
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def create_database(user, password):
    print(f"Step 1: Creating database '{DB_NAME}'...")
    # Connect to 'postgres' database to create new db
    conn = get_connection(dbname="postgres", user=user, password=password)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    try:
        # Check if database exists
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
        exists = cur.fetchone()
        
        if not exists:
            cur.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"Database '{DB_NAME}' created successfully.")
        else:
            print(f"Database '{DB_NAME}' already exists. Skipping creation.")
            
    except psycopg2.Error as e:
        print(f"Error creating database: {e}")
        sys.exit(1)
    finally:
        cur.close()
        conn.close()

def run_sql_file(filename, user, password):
    print(f"\nStep: Running SQL file '{filename}'...")
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
        
    conn = get_connection(dbname=DB_NAME, user=user, password=password)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    try:
        with open(filename, 'r') as f:
            sql_content = f.read()
            cur.execute(sql_content)
            print(f"Successfully executed '{filename}'.")
    except psycopg2.Error as e:
        print(f"Error executing SQL file: {e}")
        sys.exit(1)
    finally:
        cur.close()
        conn.close()

def main():
    print("Setting up Kabarak Lost and Found Database...")
    
    # Get password securely
    password = os.environ.get("PG_PASSWORD")
    if not password:
        try:
            password = getpass.getpass(prompt=f"Enter password for user '{DB_USER}': ")
        except Exception:
            # Fallback for environments where getpass might fail (though unlikely in terminal)
            password = input(f"Enter password for user '{DB_USER}': ")

    # 1. Create Database
    create_database(DB_USER, password)
    
    # 2. Apply Schema
    run_sql_file(SCHEMA_FILE, DB_USER, password)
    
    # 3. Apply Seed Data
    run_sql_file(SEED_FILE, DB_USER, password)
    
    print("\nDatabase setup complete!")

if __name__ == "__main__":
    main()
