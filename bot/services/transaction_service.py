"""Transaction service for database operations"""

import logging
from typing import List, Optional
from bot.models.database import Database
from bot.models.transaction import Transaction

logger = logging.getLogger(__name__)


class TransactionService:
    """Service for transaction-related database operations"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def create(
        self,
        from_user_id: int,
        to_user_id: int,
        amount: float,
        balance_from: float,
        balance_to: float,
        message_id: int = None,
        group_id: int = None
    ) -> Transaction:
        """Create a new transaction"""
        cursor = self.db.execute(
            """
            INSERT INTO transactions 
            (from_user_id, to_user_id, amount, balance_from, balance_to, message_id, group_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (from_user_id, to_user_id, amount, balance_from, balance_to, message_id, group_id)
        )
        transaction_id = cursor.lastrowid
        logger.info(
            f"Created transaction {transaction_id}: "
            f"User {from_user_id} -> User {to_user_id}, ${amount:.2f}"
        )
        return self.get_by_id(transaction_id)
    
    def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Get transaction by ID"""
        row = self.db.fetchone(
            """
            SELECT t.*, 
                   u1.username as from_username,
                   u1.first_name as from_first_name,
                   u2.username as to_username,
                   u2.first_name as to_first_name
            FROM transactions t
            JOIN users u1 ON t.from_user_id = u1.id
            JOIN users u2 ON t.to_user_id = u2.id
            WHERE t.id = ?
            """,
            (transaction_id,)
        )
        return self._row_to_transaction(row) if row else None
    
    def get_recent(self, limit: int = 10) -> List[Transaction]:
        """Get recent transactions"""
        rows = self.db.fetchall(
            """
            SELECT t.*, 
                   u1.username as from_username,
                   u1.first_name as from_first_name,
                   u2.username as to_username,
                   u2.first_name as to_first_name
            FROM transactions t
            JOIN users u1 ON t.from_user_id = u1.id
            JOIN users u2 ON t.to_user_id = u2.id
            ORDER BY t.created_at DESC
            LIMIT ?
            """,
            (limit,)
        )
        return [self._row_to_transaction(row) for row in rows]
    
    def get_by_user(self, user_id: int, limit: int = 10) -> List[Transaction]:
        """Get transactions for a specific user"""
        rows = self.db.fetchall(
            """
            SELECT t.*, 
                   u1.username as from_username,
                   u1.first_name as from_first_name,
                   u2.username as to_username,
                   u2.first_name as to_first_name
            FROM transactions t
            JOIN users u1 ON t.from_user_id = u1.id
            JOIN users u2 ON t.to_user_id = u2.id
            WHERE t.from_user_id = ? OR t.to_user_id = ?
            ORDER BY t.created_at DESC
            LIMIT ?
            """,
            (user_id, user_id, limit)
        )
        return [self._row_to_transaction(row) for row in rows]
    
    def get_count(self) -> int:
        """Get total transaction count"""
        row = self.db.fetchone("SELECT COUNT(*) as count FROM transactions")
        return row['count'] if row else 0
    
    @staticmethod
    def _get_row_value(row, key: str, default=None):
        """Safely get value from sqlite3.Row object"""
        try:
            return row[key]
        except (KeyError, IndexError):
            return default
    
    def _row_to_transaction(self, row) -> Transaction:
        """Convert database row to Transaction object"""
        # Get display names
        from_username = self._get_row_value(row, 'from_username')
        from_first_name = self._get_row_value(row, 'from_first_name')
        to_username = self._get_row_value(row, 'to_username')
        to_first_name = self._get_row_value(row, 'to_first_name')
        
        from_display = f"@{from_username}" if from_username else from_first_name or "Unknown"
        to_display = f"@{to_username}" if to_username else to_first_name or "Unknown"
        
        return Transaction(
            id=row['id'],
            from_user_id=row['from_user_id'],
            to_user_id=row['to_user_id'],
            amount=row['amount'],
            balance_from=row['balance_from'],
            balance_to=row['balance_to'],
            created_at=row['created_at'],
            from_user_name=from_display,
            to_user_name=to_display
        )
