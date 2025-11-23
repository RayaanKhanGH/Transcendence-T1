#!/usr/bin/env python3
"""
Setup script for Transcendence T1 PostgreSQL database
"""
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv()

def create_database():
    """Create the transcendence database if it doesn't exist."""
    postgres_uri = os.getenv("POSTGRES_URI")
    
    if not postgres_uri:
        print("❌ POSTGRES_URI not found in .env")
        return False
    
    # Parse the URI to get connection details
    # Format: postgresql://user:password@host:port/dbname
    try:
        from urllib.parse import urlparse
        parsed = urlparse(postgres_uri)
        
        user = parsed.username
        password = parsed.password
        host = parsed.hostname
        port = parsed.port or 5432
        dbname = parsed.path[1:]  # Remove leading /
        
        print(f"Connecting to PostgreSQL at {host}:{port}...")
        
        # Connect to default 'postgres' database to create our database
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
        exists = cursor.fetchone()
        
        if exists:
            print(f"✅ Database '{dbname}' already exists")
        else:
            cursor.execute(f'CREATE DATABASE "{dbname}"')
            print(f"✅ Database '{dbname}' created successfully!")
        
        cursor.close()
        conn.close()
        
        # Now connect to the new database and create tables
        print(f"\nConnecting to '{dbname}' database...")
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=dbname
        )
        cursor = conn.cursor()
        
        # Create intelligence table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS intelligence (
                id SERIAL PRIMARY KEY,
                source_url TEXT NOT NULL,
                content TEXT,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_intelligence_url 
            ON intelligence(source_url)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_intelligence_created 
            ON intelligence(created_at DESC)
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Table 'intelligence' created successfully!")
        print("✅ Indexes created successfully!")
        print("\n🎉 Database setup complete! You can now run: python cli.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    create_database()
