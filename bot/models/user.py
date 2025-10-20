"""User model"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """User domain model"""
    
    id: Optional[int]
    name: str
    balance: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def can_debit(self, amount: float) -> bool:
        """Check if user has sufficient balance"""
        return self.balance >= amount
    
    def validate_balance(self, amount: float):
        """Validate balance amount"""
        if amount < 0:
            raise ValueError("Balance cannot be negative")
    
    @staticmethod
    def format_name(name: str) -> str:
        """Format user name for display"""
        return name.replace('_', ' ').title()
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, balance=${self.balance:.2f})"
