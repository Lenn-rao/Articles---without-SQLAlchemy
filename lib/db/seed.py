from .connection import get_connection

def seed_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    
    # Seed authors
    authors = [("Jane Doe",), ("John Smith",), ("Alice Johnson",)]
    cursor.executemany("INSERT INTO authors (name) VALUES (?)", authors)
    
    # Seed magazines
    magazines = [
        ("Tech Today", "Technology"),
        ("Science Weekly", "Science"),
        ("Culture Mag", "Culture")
    ]
    cursor.executemany("INSERT INTO magazines (name, category) VALUES (?, ?)", magazines)
    
    # Seed articles
    articles = [
        ("Tech Trends 2025", 1, 1),
        ("AI Revolution", 1, 2),
        ("Quantum Computing", 2, 1),
        ("Cultural Shifts", 3, 3),
        ("Science Breakthroughs", 2, 2)
    ]
    cursor.executemany("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", articles)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_database()