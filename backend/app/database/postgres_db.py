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
                );
            """)
                cur.execute("""
            CREATE TABLE IF NOT EXISTS collaborations (
            id SERIAL PRIMARY KEY,
            source_brand TEXT NOT NULL,
            target_brand TEXT NOT NULL,
            plastic_type TEXT,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
            """)
                
                cur.execute("""
            CREATE TABLE IF NOT EXISTS collaboration_products (
            id SERIAL PRIMARY KEY,
            collaboration_id INTEGER REFERENCES collaborations(id) ON DELETE CASCADE,
            product_type TEXT,
            product_name TEXT,
            product_description TEXT,
            pitch TEXT,
            image_url TEXT,
            full_result JSONB
);
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
    
    def create_or_get_collaboration(self, source_brand, target_brand, plastic_type, location) -> int:
        conn = self._get_connection()
        source_brand = source_brand.lower()
        target_brand = target_brand.lower()
        plastic_type = plastic_type.lower()
        location = location.lower()

        try:
            with conn.cursor() as cur:
                # Try to find existing collaboration
                cur.execute("""
                    SELECT id FROM collaborations
                    WHERE source_brand = %s AND target_brand = %s
                      AND plastic_type = %s AND location = %s
                    LIMIT 1
                """, (source_brand, target_brand, plastic_type, location))
                row = cur.fetchone()

                if row:
                    return row[0]  # Collaboration exists
                else:
                    # Insert new collaboration
                    cur.execute("""
                        INSERT INTO collaborations (source_brand, target_brand, plastic_type, location)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id
                    """, (source_brand, target_brand, plastic_type, location))
                    new_id = cur.fetchone()[0]
                    conn.commit()
                    return new_id
        except Exception as e:
            print(f"Error creating/finding collaboration: {e}")
            raise
        finally:
            conn.close()


    def add_collaboration_product(self, collaboration_id: int, data: Dict) -> int:
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO collaboration_products (
                        collaboration_id, product_name, product_type,
                        product_description, pitch, image_url, full_result
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    collaboration_id,
                    data["product_name"],
                    data.get("product_type"),
                    data.get("product_description"),
                    data.get("pitch"),
                    data.get("image_url"),
                    Json(data["full_result"])  # Make sure it's a dict
                ))
                product_id = cur.fetchone()[0]
                conn.commit()
                return product_id
        except Exception as e:
            print(f"Error saving product: {e}")
            raise
        finally:
            conn.close()

    def get_collaboration_with_products(self, source_brand, target_brand, plastic_type, location) -> Optional[Dict]:
        conn = self._get_connection()
        print(f"Searching for collaboration with: source_brand='{source_brand}', "
              f"target_brand='{target_brand}', plastic_type='{plastic_type}', location='{location}'")
        try:
            with conn.cursor() as cur:
                # Search for the collaboration record
                cur.execute("""
                    SELECT id FROM collaborations
    WHERE LOWER(source_brand) = LOWER(%s)
      AND LOWER(target_brand) = LOWER(%s)
      AND LOWER(plastic_type) = LOWER(%s)
      AND LOWER(location) = LOWER(%s)
    LIMIT 1
                """, (source_brand, target_brand, plastic_type, location))
                row = cur.fetchone()

                if not row:
                    print("No collaboration found for the given criteria.")
                    return None

                collaboration_id = row[0]
                print(f"Found collaboration with ID: {collaboration_id}")

                # Fetch associated products
                cur.execute("""
                    SELECT product_name, product_type, product_description, pitch, image_url
                    FROM collaboration_products
                    WHERE collaboration_id = %s
                """, (collaboration_id,))
                products = cur.fetchall()

                print(f"Retrieved {len(products)} products for collaboration ID {collaboration_id}")

                product_keys = ["product_name", "product_type", "product_description", "pitch", "image_url"]
                product_dicts = [dict(zip(product_keys, p)) for p in products]

                return {
                    "collaboration_id": collaboration_id,
                    "source_brand": source_brand,
                    "target_brand": target_brand,
                    "plastic_type": plastic_type,
                    "location": location,
                    "products": product_dicts
                }

        except Exception as e:
            print(f"Error fetching existing collaboration: {e}")
            return None
        finally:
            conn.close()
            
    def get_collaboration_product_count(self, collaboration_id: int) -> int:
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COUNT(*) FROM collaboration_products
                    WHERE collaboration_id = %s
                """, (collaboration_id,))
                count = cur.fetchone()[0]
                return count
        except Exception as e:
            print(f"Error counting products: {e}")
            return 0
        finally:
            conn.close()

    def delete_products_for_collaboration(self, collaboration_id: int):
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM collaboration_products
                    WHERE collaboration_id = %s
                """, (collaboration_id,))
                conn.commit()
        except Exception as e:
            print(f"Error deleting products: {e}")
            raise
        finally:
            conn.close()
