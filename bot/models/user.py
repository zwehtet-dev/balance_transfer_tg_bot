"""User model"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """User domain model with Telegram info"""
    
    id: Optional[int]
    telegram_user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
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
    
    @property
    def display_name(self) -> str:
        """Get display name for user"""
        if self.username:
            return f"@{self.username}"
        elif self.first_name:
            name = self.first_name
            if self.last_name:
                name += f" {self.last_name}"
            return name
        else:
            return f"User {self.telegram_user_id}"
    
    @property
    def mention(self) -> str:
        """Get mention string for Telegram"""
        if self.username:
            return f"@{self.username}"
        else:
            return self.display_name
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, telegram_id={self.telegram_user_id}, username={self.username}, balance=${self.balance:.2f})"
