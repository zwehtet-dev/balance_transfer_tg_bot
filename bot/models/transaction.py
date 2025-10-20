"""Transaction model"""

from dataclasses import dataclass
from typing import Optional, Union
from datetime import datetime


@dataclass
class Transaction:
    """Transaction domain model"""
    
    id: Optional[int]
    from_user_id: int
    to_user_id: int
    amount: float
    balance_from: float
    balance_to: float
    created_at: Optional[Union[datetime, str]] = None  # Can be datetime or string from SQLite
    
    # Optional fields for display
    from_user_name: Optional[str] = None
    to_user_name: Optional[str] = None
    
    def format_display(self) -> str:
        """Format transaction for display"""
        from_name = self._format_name(self.from_user_name or f"User {self.from_user_id}")
        to_name = self._format_name(self.to_user_name or f"User {self.to_user_id}")
        
        # Handle both datetime objects and string timestamps from SQLite
        if self.created_at:
            if isinstance(self.created_at, str):
                timestamp = self.created_at
            else:
                timestamp = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        else:
            timestamp = "N/A"
        
        return (
            f"💸 ${self.amount:.2f} | {from_name} → {to_name}\n"
            f"   {timestamp}"
        )
    
    @staticmethod
    def _format_name(name: str) -> str:
        """Format name for display"""
        return name.replace('_', ' ').title()
    
    def __repr__(self) -> str:
        return (
            f"Transaction(id={self.id}, from={self.from_user_id}, "
            f"to={self.to_user_id}, amount=${self.amount:.2f})"
        )
