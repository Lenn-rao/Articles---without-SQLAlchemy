import pytest
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

def test_magazine_creation(setup_db):
    magazine = Magazine("New Mag", "News")
    assert magazine.id is not None
    assert magazine.name == "New Mag"
    assert magazine.category == "News"

def test_magazine_validation(setup_db):
    with pytest.raises(ValueError):
        Magazine("", "News")

def test_magazine_articles(setup_db):
    magazine = Magazine.find_by_name("Tech Today")
    articles = magazine.articles()
    assert len(articles) == 2
    assert any(a['title'] == "Tech Trends 2025" for a in articles)

def test_magazine_contributors(setup_db):
    magazine = Magazine.find_by_name("Tech Today")
    contributors = magazine.contributors()
    assert len(contributors) == 2
    assert any(c['name'] == "Jane Doe" for c in contributors)

def test_magazine_article_titles(setup_db):
    magazine = Magazine.find_by_name("Tech Today")
    titles = magazine.article_titles()
    assert "Tech Trends 2025" in titles
    assert "Quantum Computing" in titles

def test_magazine_top_publisher(setup_db):
    magazine = Magazine.top_publisher()
    assert magazine.name in ["Tech Today", "Science Weekly"]  # Both have 2 articles