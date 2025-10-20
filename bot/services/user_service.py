"""User service for database operations"""

import logging
from typing import Optional, List
from bot.models.database import Database
from bot.models.user import User

logger = logging.getLogger(__name__)


class UserService:
    """Service for user-related database operations"""
    
    def __init__(self, db: Database, default_balance: float = 1000.0):
        self.db = db
        self.default_balance = default_balance
    
    def get_or_create_user(
        self,
        telegram_user_id: int,
        username: str = None,
        first_name: str = None,
        last_name: str = None
    ) -> User:
        """Get existing user or create new one with default balance"""
        # Try to get existing user
        user = self.get_by_telegram_id(telegram_user_id)
        
        if user:
            # Update user info if changed
            if username != user.username or first_name != user.first_name:
                self.update_user_info(user.id, username, first_name, last_name)
                user = self.get_by_telegram_id(telegram_user_id)
            return user
        
        # Create new user with default balance
        logger.info(f"Creating new user: {username or first_name} (ID: {telegram_user_id})")
        cursor = self.db.execute(
            """
            INSERT INTO users (telegram_user_id, username, first_name, last_name, balance)
            VALUES (?, ?, ?, ?, ?)
            """,
            (telegram_user_id, username, first_name, last_name, self.default_balance)
        )
        user_id = cursor.lastrowid
        logger.info(f"Created user {user_id} with balance ${self.default_balance:.2f}")
        return self.get_by_id(user_id)
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by internal ID"""
        row = self.db.fetchone(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )
        return self._row_to_user(row) if row else None
    
    def get_by_telegram_id(self, telegram_user_id: int) -> Optional[User]:
        """Get user by Telegram user ID"""
        row = self.db.fetchone(
            "SELECT * FROM users WHERE telegram_user_id = ?",
            (telegram_user_id,)
        )
        return self._row_to_user(row) if row else None
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username (without @) or first name"""
        if not username:
            return None
        
        # Clean username
        username_clean = username.lower().replace('@', '').strip()
        
        # Try exact username match first
        row = self.db.fetchone(
            "SELECT * FROM users WHERE LOWER(username) = ?",
            (username_clean,)
        )
        if row:
            return self._row_to_user(row)
        
        # Try first name match (case-insensitive, partial match)
        row = self.db.fetchone(
            "SELECT * FROM users WHERE LOWER(first_name) LIKE ?",
            (f"%{username_clean}%",)
        )
        if row:
            return self._row_to_user(row)
        
        # Try last name match
        row = self.db.fetchone(
            "SELECT * FROM users WHERE LOWER(last_name) LIKE ?",
            (f"%{username_clean}%",)
        )
        return self._row_to_user(row) if row else None
    
    def get_all(self) -> List[User]:
        """Get all users"""
        rows = self.db.fetchall("SELECT * FROM users ORDER BY created_at")
        return [self._row_to_user(row) for row in rows]
    
    def update_balance(self, user_id: int, new_balance: float) -> bool:
        """Update user balance"""
        if new_balance < 0:
            raise ValueError("Balance cannot be negative")
        
        self.db.execute(
            "UPDATE users SET balance = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (new_balance, user_id)
        )
        logger.info(f"Updated balance for user {user_id}: ${new_balance:.2f}")
        return True
    
    def update_user_info(
        self,
        user_id: int,
        username: str = None,
        first_name: str = None,
        last_name: str = None
    ):
        """Update user information"""
        self.db.execute(
            """
            UPDATE users 
            SET username = ?, first_name = ?, last_name = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (username, first_name, last_name, user_id)
        )
    
    def get_user_count(self) -> int:
        """Get total user count"""
        row = self.db.fetchone("SELECT COUNT(*) as count FROM users")
        return row['count'] if row else 0
    
    @staticmethod
    def _row_to_user(row) -> User:
        """Convert database row to User object"""
        return User(
            id=row['id'],
            telegram_user_id=row['telegram_user_id'],
            username=row['username'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            balance=row['balance'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
