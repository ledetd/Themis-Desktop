import sqlite3
from database_manager import db_manager

def init_db():
    try:
        conn = db_manager.get_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                category TEXT NOT NULL,
                name TEXT NOT NULL,
                part_number TEXT NOT NULL,
                description TEXT,
                quantity INTEGER
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_category ON products (category)")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as e:
        print(f"Database initialization error: {e}")

def get_items_from_db(category=None):
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        if category:
            cursor.execute("SELECT id, category, name, part_number, description, quantity FROM products WHERE category = ?", (category,))
        else:
            cursor.execute("SELECT * FROM products")
        items = cursor.fetchall()
        conn.close()
        return items
    except sqlite3.DatabaseError as e:
        print(f"Error fetching items from DB: {e}")
        return []

def get_all_categories():
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM products")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories
    except sqlite3.DatabaseError as e:
        print(f"Error fetching categories: {e}")
        return []

def get_products():
    try:
        conn = db_manager.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products ORDER BY category ASC")
        products = cur.fetchall()
        conn.close()
        return products
    except sqlite3.DatabaseError as e:
        print(f"Error fetching products: {e}")
        return []

def add_product(category, name, part_number, description, quantity):
    try:
        conn = db_manager.get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO products (category, name, part_number, description, quantity) VALUES (?, ?, ?, ?, ?)", 
                    (category, name, part_number, description, quantity))
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as e:
        print(f"Error adding product: {e}")

def edit_product(product_id, category, name, part_number, description, quantity):
    try:
        conn = db_manager.get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE products
            SET category = ?, name = ?, part_number = ?, description = ?, quantity = ?
            WHERE id = ?
        """, (category, name, part_number, description, quantity, product_id))
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as e:
        print(f"Error editing product: {e}")

def delete_product(product_id):
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as e:
        print(f"Error deleting product: {e}")
