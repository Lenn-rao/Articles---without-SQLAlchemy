import pytest
from lib.models.author import Author
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

def test_author_creation(setup_db):
    author = Author("Test Author")
    assert author.id is not None
    assert author.name == "Test Author"

def test_author_validation(setup_db):
    with pytest.raises(ValueError):
        Author("")

def test_author_articles(setup_db):
    author = Author.find_by_name("Jane Doe")
    articles = author.articles()
    assert len(articles) == 2
    assert any(a['title'] == "Tech Trends 2025" for a in articles)

def test_author_magazines(setup_db):
    author = Author.find_by_name("Jane Doe")
    magazines = author.magazines()
    assert len(magazines) == 2
    assert any(m['name'] == "Tech Today" for m in magazines)

def test_author_topic_areas(setup_db):
    author = Author.find_by_name("Jane Doe")
    topics = author.topic_areas()
    assert set(topics) == {"Technology", "Science"}

def test_author_most_articles(setup_db):
    author = Author.most_articles()
    assert author.name in ["Jane Doe", "John Smith"]  # Both have 2 articles in seed data