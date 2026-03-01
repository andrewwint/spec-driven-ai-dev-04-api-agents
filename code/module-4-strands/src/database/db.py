"""
SQLite Database Connection.

Local-first with PostgreSQL upgrade path.
"""

import sqlite3
from contextlib import contextmanager
import os

DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/app.db')


@contextmanager
def get_connection():
    """Context manager for database connections."""
    db_path = os.getenv('DATABASE_PATH', DATABASE_PATH)
    os.makedirs(os.path.dirname(db_path) or '.', exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Initialize database schema."""
    with get_connection() as conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER REFERENCES customers(id),
                prediction TEXT NOT NULL,
                confidence REAL NOT NULL,
                request_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_predictions_customer ON predictions(customer_id);
        ''')
        conn.commit()


def reset_db():
    """Reset database (for testing)."""
    db_path = os.getenv('DATABASE_PATH', DATABASE_PATH)
    if os.path.exists(db_path):
        os.remove(db_path)
    init_db()
