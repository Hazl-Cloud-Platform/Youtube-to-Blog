import sqlite3
import os

class DatabaseHandler:
    def __init__(self):
        self.db_path = "user_settings.db"
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_keys
            (id INTEGER PRIMARY KEY,
             openai_key TEXT)
        ''')
        conn.commit()
        conn.close()

    def save_api_key(self, api_key):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM api_keys")  # Remove old key
        cursor.execute("INSERT INTO api_keys (openai_key) VALUES (?)", (api_key,))
        conn.commit()
        conn.close()

    def get_api_key(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT openai_key FROM api_keys LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None 