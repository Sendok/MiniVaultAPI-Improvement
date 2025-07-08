import sqlite3        # For interacting with the SQLite database
import json           # For formatting logs as JSON
import os             # For file path operations
from datetime import datetime  # To timestamp logs

# Define the path to the SQLite database file (relative to this script's location)
DB_PATH = os.path.join(os.path.dirname(__file__), "../db/minivault.db")

# Define the path to the log file (line-delimited JSON)
LOG_FILE = "logs/log.jsonl"

# Ensure the "logs" directory exists, create it if it doesn't
os.makedirs("logs", exist_ok=True)

# Logs an interaction into the SQLite database
def log_to_db(prompt: str, response: str):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create the interactions table if it doesn't already exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Insert the prompt and response into the table
        cursor.execute("INSERT INTO interactions (prompt, response) VALUES (?, ?)", (prompt, response))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    except Exception as e:
        # Print error if database logging fails
        print(f"[DB Logging Error] {e}")

# Logs an interaction into a JSONL (JSON Lines) file
def log_interaction(prompt: str, response: str):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),  # Use UTC timestamp in ISO format
        "prompt": prompt,
        "response": response
    }
    try:
        # Append the JSON log to the file (each line is a separate JSON object)
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")

    except Exception as e:
        # Print error if file logging fails
        print(f"[File Logging Error] {e}")
