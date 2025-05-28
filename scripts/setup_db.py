from lib.db.connection import get_connection
from lib.db.seed import seed_database

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Read and execute schema
    with open('lib/db/schema.sql', 'r') as f:
        cursor.executescript(f.read())
    
    conn.commit()
    conn.close()
    
    # Seed database
    seed_database()

if __name__ == "__main__":
    setup_database()