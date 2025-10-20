"""Balance service for business logic"""

import logging
from dataclasses import dataclass
from typing import Optional
from bot.models.database import Database
from bot.models.transaction import Transaction
from bot.services.user_service import UserService
from bot.services.transaction_service import TransactionService

logger = logging.getLogger(__name__)


@dataclass
class TransferResult:
    """Result of a transfer operation"""
    success: bool
    message: str
    transaction: Optional[Transaction] = None


class BalanceService:
    """Service for balance and transfer operations"""
    
    def __init__(self, db: Database, default_balance: float = 1000.0):
        self.db = db
        self.user_service = UserService(db, default_balance)
        self.transaction_service = TransactionService(db)
    
    def transfer_by_user_id(
        self,
        from_user_id: int,
        to_user_id: int,
        amount: float,
        message_id: int = None,
        group_id: int = None
    ) -> TransferResult:
        """
        Transfer amount between users by their internal IDs
        
        Args:
            from_user_id: Internal user ID of sender
            to_user_id: Internal user ID of receiver
            amount: Amount to transfer
            message_id: Telegram message ID (optional)
            group_id: Telegram group ID (optional)
        
        Returns:
            TransferResult with success status and message
        """
        try:
            # Validation
            if amount <= 0:
                return TransferResult(False, "❌ Transfer amount must be positive!")
            
            # Get users
            from_user = self.user_service.get_by_id(from_user_id)
            to_user = self.user_service.get_by_id(to_user_id)
            
            if not from_user:
                return TransferResult(False, f"❌ Sender not found!")
            
            if not to_user:
                return TransferResult(False, f"❌ Receiver not found!")
            
            if from_user.id == to_user.id:
                return TransferResult(False, "❌ Cannot transfer to yourself!")
            
            if not from_user.can_debit(amount):
                return TransferResult(
                    False,
                    f"❌ Insufficient funds! "
                    f"{from_user.display_name} has ${from_user.balance:.2f}"
                )
            
            # Perform transfer (atomic operation)
            new_balance_from = from_user.balance - amount
            new_balance_to = to_user.balance + amount
            
            # Update balances
            self.user_service.update_balance(from_user.id, new_balance_from)
            self.user_service.update_balance(to_user.id, new_balance_to)
            
            # Record transaction
            transaction = self.transaction_service.create(
                from_user_id=from_user.id,
                to_user_id=to_user.id,
                amount=amount,
                balance_from=new_balance_from,
                balance_to=new_balance_to,
                message_id=message_id,
                group_id=group_id
            )
            
            message = (
                f"✅ Transfer successful!\n\n"
                f"💸 ${amount:.2f} from {from_user.display_name} to {to_user.display_name}"
            )
            
            logger.info(
                f"Transfer: {from_user.display_name} -> {to_user.display_name}, "
                f"amount: ${amount:.2f}"
            )
            return TransferResult(True, message, transaction)
            
        except Exception as e:
            logger.error(f"Transfer error: {e}", exc_info=True)
            return TransferResult(False, f"❌ Transfer failed: {str(e)}")
    
    def get_all_balances(self) -> str:
        """Get formatted string of all balances"""
        users = self.user_service.get_all()
        
        if not users:
            return "❌ No users found in the system."
        
        # Sort by balance descending
        users.sort(key=lambda u: u.balance, reverse=True)
        
        total = sum(user.balance for user in users)
        
        balance_text = "💰 All Balances:\n\n"
        for i, user in enumerate(users, 1):
            balance_text += f"{i}. {user.display_name}: ${user.balance:.2f}\n"
        
        balance_text += f"\n📊 Total: ${total:.2f}"
        balance_text += f"\n👥 Users: {len(users)}"
        
        return balance_text
    
    def get_transaction_history(self, limit: int = 10) -> str:
        """Get formatted transaction history"""
        transactions = self.transaction_service.get_recent(limit)
        
        if not transactions:
            return "📊 No transactions yet."
        
        history = f"📊 Recent Transactions (Last {len(transactions)}):\n\n"
        for i, transaction in enumerate(transactions, 1):
            history += f"{i}. {transaction.format_display()}\n"
        
        return history
    
    def get_user_balance(self, telegram_user_id: int) -> Optional[float]:
        """Get balance for a specific Telegram user"""
        user = self.user_service.get_by_telegram_id(telegram_user_id)
        return user.balance if user else None
