# Articles---without-SQLAlchemy
# Articles Code Challenge

A Python application modeling relationships between Authors, Articles, and Magazines using a SQL database (SQLite).

## Setup
1. Create virtual environment: `python -m venv env`
2. Activate: `source env/bin/activate` (Mac/Linux) or `env\Scripts\activate` (Windows)
3. Install dependencies: `pip install pytest`
4. Set up database: `python scripts/setup_db.py`
5. Run tests: `pytest`

## Features
- Models: Author, Article, Magazine with SQL-based persistence
- Relationships: Many-to-many between Authors and Magazines via Articles
- Transaction handling for data integrity
- Comprehensive test suite