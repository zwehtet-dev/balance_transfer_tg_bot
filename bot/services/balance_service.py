"""Balance service for business logic"""

import logging
from dataclasses import dataclass
from typing import Optional
from bot.models.database import Database
from bot.models.user import User
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
    
    def __init__(self, db: Database):
        self.db = db
        self.user_service = UserService(db)
        self.transaction_service = TransactionService(db)
    
    def transfer(self, from_name: str, to_name: str, amount: float) -> TransferResult:
        """
        Transfer amount from one user to another
        Returns: TransferResult with success status and message
        """
        try:
            # Validation
            if amount <= 0:
                return TransferResult(False, "❌ Transfer amount must be positive!")
            
            # Get users
            from_user = self.user_service.get_by_name(from_name)
            to_user = self.user_service.get_by_name(to_name)
            
            if not from_user:
                return TransferResult(False, f"❌ User {from_name} not found!")
            
            if not to_user:
                return TransferResult(False, f"❌ User {to_name} not found!")
            
            if from_user.id == to_user.id:
                return TransferResult(False, "❌ Cannot transfer to the same user!")
            
            if not from_user.can_debit(amount):
                return TransferResult(
                    False,
                    f"❌ Insufficient funds! "
                    f"{User.format_name(from_name)} has ${from_user.balance:.2f}"
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
                balance_to=new_balance_to
            )
            
            message = (
                f"✅ Transfer successful!\n\n"
                f"💸 ${amount:.2f} transferred from "
                f"{User.format_name(from_name)} to "
                f"{User.format_name(to_name)}"
            )
            
            logger.info(f"Transfer: {from_name} -> {to_name}, amount: ${amount:.2f}")
            return TransferResult(True, message, transaction)
            
        except Exception as e:
            logger.error(f"Transfer error: {e}", exc_info=True)
            return TransferResult(False, f"❌ Transfer failed: {str(e)}")
    
    def get_all_balances(self) -> str:
        """Get formatted string of all balances"""
        users = self.user_service.get_all()
        
        if not users:
            return "❌ No users found in the system."
        
        total = sum(user.balance for user in users)
        
        balance_text = "💰 Current Balances:\n\n"
        for user in users:
            balance_text += f"👤 {User.format_name(user.name)}: ${user.balance:.2f}\n"
        
        balance_text += f"\n📊 Total: ${total:.2f}"
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
    
    def reset_all_balances(self, default_balance: float = 1000.0):
        """Reset all user balances to default"""
        self.user_service.reset_all_balances(default_balance)
        self.transaction_service.delete_all()
        logger.info(f"Reset all balances to ${default_balance:.2f}")
    
    def get_balance(self, name: str) -> float:
        """Get balance for a specific user"""
        user = self.user_service.get_by_name(name)
        return user.balance if user else 0.0
