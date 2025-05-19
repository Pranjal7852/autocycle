from typing import Dict
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Load environment variables
load_dotenv()

# Get database configuration from environment variables
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

class PostgresManager:
    def __init__(self):
        self.conn_params = {
            "host": POSTGRES_HOST,
            "port": POSTGRES_PORT,
            "dbname": POSTGRES_DB,
            "user": POSTGRES_USER,
            "password": POSTGRES_PASSWORD
        }
        
        # Initialize tables if they don't exist
        self._init_tables()
    
    def _get_connection(self):
        """Get a PostgreSQL connection"""
        conn = psycopg2.connect(**self.conn_params)
        conn.autocommit = True
        return conn
    
    def _init_tables(self):
        """Initialize the necessary tables if they don't exist"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                # Create brands table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS brands (
                        id SERIAL PRIMARY KEY,
                        brand_id TEXT UNIQUE NOT NULL,
                        name TEXT NOT NULL,
                        description TEXT,
                        sustainability_score FLOAT,
                        recycling_info TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create plastic types table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS plastic_types (
                        id SERIAL PRIMARY KEY,
                        plastic_id TEXT UNIQUE NOT NULL,
                        type TEXT NOT NULL,
                        description TEXT,
                        recyclable BOOLEAN,
                        biodegradable BOOLEAN,
                        decomposition_time TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
        finally:
            conn.close()
    
    def store_brand_data(self, brand_data: Dict):
        """Store brand data in PostgreSQL"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO brands (brand_id, name, description, sustainability_score, recycling_info)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (brand_id) 
                    DO UPDATE SET 
                        name = EXCLUDED.name,
                        description = EXCLUDED.description,
                        sustainability_score = EXCLUDED.sustainability_score,
                        recycling_info = EXCLUDED.recycling_info
                    RETURNING brand_id
                """, (
                    brand_data.get("brand_id"),
                    brand_data.get("name"),
                    brand_data.get("description"),
                    brand_data.get("sustainability_score"),
                    brand_data.get("recycling_info")
                ))
                result = cur.fetchone()
        finally:
            conn.close()
        return result[0] if result else None
    
    def store_plastic_data(self, plastic_data: Dict):
        """Store plastic type data in PostgreSQL"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO plastic_types (
                        plastic_id, type, description, recyclable, biodegradable, decomposition_time
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (plastic_id) 
                    DO UPDATE SET 
                        type = EXCLUDED.type,
                        description = EXCLUDED.description,
                        recyclable = EXCLUDED.recyclable,
                        biodegradable = EXCLUDED.biodegradable,
                        decomposition_time = EXCLUDED.decomposition_time
                    RETURNING plastic_id
                """, (
                    plastic_data.get("plastic_id"),
                    plastic_data.get("type"),
                    plastic_data.get("description"),
                    plastic_data.get("recyclable"),
                    plastic_data.get("biodegradable"),
                    plastic_data.get("decomposition_time")
                ))
                result = cur.fetchone()
                return result[0] if result else None
        finally:
            conn.close()
            
    def get_brand_by_id(self, brand_id: str):
        """Get brand details by brand_id"""
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM brands WHERE brand_id = %s
                """, (brand_id,))
                return cur.fetchone()
        finally:
            conn.close()
            
    def get_plastic_by_id(self, plastic_id: str):
        """Get plastic type details by plastic_id"""
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM plastic_types WHERE plastic_id = %s
                """, (plastic_id,))
                return cur.fetchone()
        finally:
            conn.close()