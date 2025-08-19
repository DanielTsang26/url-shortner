import sys
import os

# Add the parent directory (succinctly) to Python's module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import Database


db = Database()

try:
    conn = db.connect()
    print(" Connection successful!")
    conn.close()
except Exception as e:
    print(f" Connection failed: {e}")