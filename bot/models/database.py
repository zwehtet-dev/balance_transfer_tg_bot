"""Database connection and initialization"""

import sqlite3
import logging
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class Database:
    """SQLite database manager with connection pooling"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self._ensure_directory()
        self._connection: Optional[sqlite3.Connection] = None
    
    def _ensure_directory(self):
        """Ensure database directory exists"""
        db_path = Path(self.database_url)
        db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def connect(self) -> sqlite3.Connection:
        """Get or create database connection"""
        if self._connection is None:
            self._connection = sqlite3.connect(
                self.database_url,
                check_same_thread=False,
                isolation_level=None  # Autocommit mode
            )
            self._connection.row_factory = sqlite3.Row
            logger.info(f"Connected to database: {self.database_url}")
        return self._connection
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = self.connect()
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self._connection:
            self._connection.close()
            self._connection = None
            logger.info("Database connection closed")
    
    def execute(self, query: str, params: tuple = ()):
        """Execute a query and return cursor"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor
    
    def fetchone(self, query: str, params: tuple = ()):
        """Execute query and fetch one result"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
    
    def fetchall(self, query: str, params: tuple = ()):
        """Execute query and fetch all results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()


def init_database(db: Database):
    """Initialize database schema for group-based bot"""
    logger.info("Initializing database schema...")
    
    # Create users table with Telegram user info
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_user_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            balance REAL NOT NULL DEFAULT 1000.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create transactions table
    db.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_user_id INTEGER NOT NULL,
            to_user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            balance_from REAL NOT NULL,
            balance_to REAL NOT NULL,
            message_id INTEGER,
            group_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (from_user_id) REFERENCES users(id),
            FOREIGN KEY (to_user_id) REFERENCES users(id)
        )
    """)
    
    # Create indexes
    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_telegram_id 
        ON users(telegram_user_id)
    """)
    
    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_transactions_from_user 
        ON transactions(from_user_id)
    """)
    
    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_transactions_to_user 
        ON transactions(to_user_id)
    """)
    
    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_transactions_created_at 
        ON transactions(created_at DESC)
    """)
    
    logger.info("Database schema initialized successfully")
