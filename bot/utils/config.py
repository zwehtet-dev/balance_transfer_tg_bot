"""Configuration management for the bot"""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BotConfig:
    """Bot configuration settings"""
    
    # Bot token
    token: str
    
    # Database settings
    database_url: str = "data/bot.db"
    
    # User settings
    default_balance: float = 1000.0
    max_transaction_history: int = 10
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: str = "logs/bot.log"
    
    @classmethod
    def from_env(cls) -> "BotConfig":
        """Load configuration from environment variables"""
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN environment variable is required. "
                "Get your token from @BotFather on Telegram."
            )
        
        database_url = os.getenv("DATABASE_URL", "data/bot.db")
        default_balance = float(os.getenv("DEFAULT_BALANCE", "1000.0"))
        max_history = int(os.getenv("MAX_TRANSACTION_HISTORY", "10"))
        log_level = os.getenv("LOG_LEVEL", "INFO")
        log_file = os.getenv("LOG_FILE", "logs/bot.log")
        
        return cls(
            token=token,
            database_url=database_url,
            default_balance=default_balance,
            max_transaction_history=max_history,
            log_level=log_level,
            log_file=log_file
        )
    
    def ensure_directories(self):
        """Ensure required directories exist"""
        # Database directory
        Path(self.database_url).parent.mkdir(parents=True, exist_ok=True)
        
        # Log directory
        Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
