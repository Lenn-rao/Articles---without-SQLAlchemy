from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name
        if id is None:
            self.save()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cursor.lastrowid
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [dict(article) for article in articles]

    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return [dict(magazine) for magazine in magazines]

    def add_article(self, magazine, title):
        return Article(title=title, author_id=self.id, magazine_id=magazine.id)

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        categories = [row['category'] for row in cursor.fetchall()]
        conn.close()
        return categories

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        author = cursor.fetchone()
        conn.close()
        return cls(author['name'], author['id']) if author else None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        author = cursor.fetchone()
        conn.close()
        return cls(author['name'], author['id']) if author else None

    @classmethod
    def most_articles(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.* FROM authors a
            JOIN articles art ON a.id = art.author_id
            GROUP BY a.id
            ORDER BY COUNT(art.id) DESC
            LIMIT 1
        """)
        author = cursor.fetchone()
        conn.close()
        return cls(author['name'], author['id']) if author else None