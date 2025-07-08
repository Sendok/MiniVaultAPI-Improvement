import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "../db/minivault.db")
LOG_FILE = "logs/log.jsonl"

# Pastikan direktori log tersedia
os.makedirs("logs", exist_ok=True)

def log_to_db(prompt: str, response: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Buat tabel jika belum ada
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("INSERT INTO interactions (prompt, response) VALUES (?, ?)", (prompt, response))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB Logging Error] {e}")

def log_interaction(prompt: str, response: str):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": prompt,
        "response": response
    }
    try:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"[File Logging Error] {e}")
