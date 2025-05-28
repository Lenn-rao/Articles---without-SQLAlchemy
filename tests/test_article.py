import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.seed import seed_database
from lib.db.connection import get_connection

@pytest.fixture
def setup_db():
    seed_database()
    yield
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

def test_article_creation(setup_db):
    author = Author("Test Author")
    magazine = Magazine("Test Mag", "Test")
    article = Article("Test Article", author.id, magazine.id)
    assert article.id is not None
    assert article.title == "Test Article"
    assert article.author_id == author.id
    assert article.magazine_id == magazine.id

def test_article_validation(setup_db):
    author = Author("Test Author")
    magazine = Magazine("Test Mag", "Test")
    with pytest.raises(ValueError):
        Article("", author.id, magazine.id)
    with pytest.raises(ValueError):
        Article("Test", -1, magazine.id)