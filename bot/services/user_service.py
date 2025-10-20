"""User service for database operations"""

import logging
from typing import Optional, List
from bot.models.database import Database
from bot.models.user import User

logger = logging.getLogger(__name__)


class UserService:
    """Service for user-related database operations"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        row = self.db.fetchone(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )
        return self._row_to_user(row) if row else None
    
    def get_by_name(self, name: str) -> Optional[User]:
        """Get user by name"""
        row = self.db.fetchone(
            "SELECT * FROM users WHERE name = ?",
            (name,)
        )
        return self._row_to_user(row) if row else None
    
    def get_all(self) -> List[User]:
        """Get all users"""
        rows = self.db.fetchall("SELECT * FROM users ORDER BY name")
        return [self._row_to_user(row) for row in rows]
    
    def create(self, name: str, balance: float = 0.0) -> User:
        """Create a new user"""
        cursor = self.db.execute(
            "INSERT INTO users (name, balance) VALUES (?, ?)",
            (name, balance)
        )
        user_id = cursor.lastrowid
        logger.info(f"Created user: {name} (ID: {user_id})")
        return self.get_by_id(user_id)
    
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
    
    def delete(self, user_id: int) -> bool:
        """Delete a user"""
        self.db.execute("DELETE FROM users WHERE id = ?", (user_id,))
        logger.info(f"Deleted user {user_id}")
        return True
    
    def reset_all_balances(self, default_balance: float = 1000.0):
        """Reset all user balances to default"""
        self.db.execute(
            "UPDATE users SET balance = ?, updated_at = CURRENT_TIMESTAMP",
            (default_balance,)
        )
        logger.info(f"Reset all balances to ${default_balance:.2f}")
    
    @staticmethod
    def _row_to_user(row) -> User:
        """Convert database row to User object"""
        return User(
            id=row['id'],
            name=row['name'],
            balance=row['balance'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
