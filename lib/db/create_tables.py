# lib/db/create_tables.py
import sqlite3
from lib.db.connection import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        bio TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS magazines (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        category TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY,
        title TEXT,
        content TEXT,
        author_id INTEGER,
        magazine_id INTEGER,
        FOREIGN KEY(author_id) REFERENCES authors(id),
        FOREIGN KEY(magazine_id) REFERENCES magazines(id)
    );
    """)

    conn.commit()
    conn.close()
