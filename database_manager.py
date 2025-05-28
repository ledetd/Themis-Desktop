import os
import sqlite3

PROJECTS_DIR = "projects"

if not os.path.exists(PROJECTS_DIR):
    os.makedirs(PROJECTS_DIR)

class DatabaseManager:
    def __init__(self):
        self.current_project = None
        self.current_db_path = None

    def switch_project(self, project_name):
        os.makedirs(PROJECTS_DIR, exist_ok=True)
        self.current_project = project_name
        self.current_db_path = os.path.join(PROJECTS_DIR, f"{project_name}.db")
        if not os.path.exists(self.current_db_path):
            conn = sqlite3.connect(self.current_db_path)
            conn.close()
        else:
            self.init_db()

    def get_current_project_name(self):
        if self.current_project is None:
            raise Exception("No project selected")
        return self.current_project

    def init_db(self):
        if not self.current_db_path:
            raise Exception("No project selected")

        conn = sqlite3.connect(self.current_db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                category TEXT NOT NULL,
                name TEXT NOT NULL,
                part_number TEXT NOT NULL,
                description TEXT,
                quantity INTEGER
            )
        """)

        conn.commit()
        conn.close()

    def get_connection(self):
        if not self.current_db_path:
            raise Exception("No project selected")
        try:
            conn = sqlite3.connect(self.current_db_path)
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

db_manager = DatabaseManager()