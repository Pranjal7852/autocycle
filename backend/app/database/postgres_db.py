from typing import Dict, Optional
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor, Json

# Load env vars
load_dotenv()

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
        self._init_tables()

    def _get_connection(self):
        conn = psycopg2.connect(**self.conn_params)
        conn.autocommit = True
        return conn

    def _init_tables(self):
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                # Brands table updated to include industry
                cur.execute("""
                CREATE TABLE IF NOT EXISTS brands (
                id SERIAL PRIMARY KEY,
                brand_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                industry TEXT,
                product_categories JSONB,
                plastic_materials JSONB,
                sustainability_philosophy TEXT,
                key_partners_or_collaborators JSONB,
                manufacturing_regions JSONB,
                brand_positioning TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
            """)

                # Plastic types table with JSONB fields for properties & applications
                cur.execute("""
               CREATE TABLE IF NOT EXISTS plastic_types (
                id SERIAL PRIMARY KEY,
                plastic_id TEXT UNIQUE NOT NULL,
                type TEXT NOT NULL,
                properties JSONB,
                applications JSONB,
                environmental_impact TEXT,
                recycling_potential TEXT,
                regional_relevance TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        finally:
            conn.close()

    def store_brand_data(self, brand_data: Dict) -> Optional[str]:
        conn = self._get_connection()
        print("POSTGRES INSERT DEBUG - brand_data:", brand_data)
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO brands (
                        brand_id, name, industry,
                        product_categories, plastic_materials,
                        sustainability_philosophy,
                        key_partners_or_collaborators,
                        manufacturing_regions,
                        brand_positioning
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (brand_id) DO UPDATE SET
                        name = EXCLUDED.name,
                        industry = EXCLUDED.industry,
                        product_categories = EXCLUDED.product_categories,
                        plastic_materials = EXCLUDED.plastic_materials,
                        sustainability_philosophy = EXCLUDED.sustainability_philosophy,
                        key_partners_or_collaborators = EXCLUDED.key_partners_or_collaborators,
                        manufacturing_regions = EXCLUDED.manufacturing_regions,
                        brand_positioning = EXCLUDED.brand_positioning
                    RETURNING brand_id
                """, (
                    brand_data.get("brand_id"),
                    brand_data.get("name"),
                    brand_data.get("industry"),
                    Json(brand_data.get("product_categories")),
                    Json(brand_data.get("plastic_materials")),
                    brand_data.get("sustainability_philosophy"),
                    Json(brand_data.get("key_partners_or_collaborators")),
                    Json(brand_data.get("manufacturing_regions")),
                    brand_data.get("brand_positioning")
                ))
                result = cur.fetchone()
                return result[0] if result else None
        finally:
            conn.close()

    def store_plastic_data(self, plastic_data: Dict) -> Optional[str]:
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO plastic_types (
                        plastic_id, type, properties, applications,
                        environmental_impact, recycling_potential, regional_relevance
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (plastic_id) DO UPDATE SET
                        type = EXCLUDED.type,
                        properties = EXCLUDED.properties,
                        applications = EXCLUDED.applications,
                        environmental_impact = EXCLUDED.environmental_impact,
                        recycling_potential = EXCLUDED.recycling_potential,
                        regional_relevance = EXCLUDED.regional_relevance
                    RETURNING plastic_id
                """, (
                    plastic_data.get("plastic_id"),
                    plastic_data.get("type"),
                    Json(plastic_data.get("properties")),
                    Json(plastic_data.get("applications")),
                    plastic_data.get("environmental_impact"),
                    plastic_data.get("recycling_potential"),
                    plastic_data.get("regional_relevance"),
                ))
                result = cur.fetchone()
                return result[0] if result else None
        finally:
            conn.close()

    def get_brand_by_id(self, brand_id: str) -> Optional[Dict]:
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM brands WHERE brand_id = %s", (brand_id,))
                return cur.fetchone()
        finally:
            conn.close()

    def get_plastic_by_id(self, plastic_id: str) -> Optional[Dict]:
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM plastic_types WHERE plastic_id = %s", (plastic_id,))
                return cur.fetchone()
        finally:
            conn.close()
