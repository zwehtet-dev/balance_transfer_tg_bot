"""Configuration management for the bot"""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BotConfig:
    """Bot configuration settings"""
    
    # Bot token
    token: str
    
    # Group and user settings
    group_id: int = 0
    person_a_user_id: int = 0
    person_b_user_id: int = 0
    
    # AI settings
    ai_provider: str = "mistral"  # mistral or openai
    mistral_api_key: str = ""
    openai_api_key: str = ""
    ai_model: str = "mistral-small-latest"
    ai_temperature: float = 0.1
    enable_ai: bool = True
    
    # Group monitoring
    monitor_groups: bool = True
    auto_detect_transfers: bool = True
    
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
        
        # Group and user IDs
        group_id = int(os.getenv("TELEGRAM_GROUP_ID", "0"))
        person_a_user_id = int(os.getenv("PERSON_A_USER_ID", "0"))
        person_b_user_id = int(os.getenv("PERSON_B_USER_ID", "0"))
        
        # AI settings
        ai_provider = os.getenv("AI_PROVIDER", "mistral")
        mistral_api_key = os.getenv("MISTRAL_API_KEY", "")
        openai_api_key = os.getenv("OPENAI_API_KEY", "")
        ai_model = os.getenv("AI_MODEL", "mistral-small-latest")
        ai_temperature = float(os.getenv("AI_TEMPERATURE", "0.1"))
        enable_ai = os.getenv("ENABLE_AI", "true").lower() == "true"
        
        # Group monitoring
        monitor_groups = os.getenv("MONITOR_GROUPS", "true").lower() == "true"
        auto_detect_transfers = os.getenv("AUTO_DETECT_TRANSFERS", "true").lower() == "true"
        
        # Database and other settings
        database_url = os.getenv("DATABASE_URL", "data/bot.db")
        default_balance = float(os.getenv("DEFAULT_BALANCE", "1000.0"))
        max_history = int(os.getenv("MAX_TRANSACTION_HISTORY", "10"))
        log_level = os.getenv("LOG_LEVEL", "INFO")
        log_file = os.getenv("LOG_FILE", "logs/bot.log")
        
        return cls(
            token=token,
            group_id=group_id,
            person_a_user_id=person_a_user_id,
            person_b_user_id=person_b_user_id,
            ai_provider=ai_provider,
            mistral_api_key=mistral_api_key,
            openai_api_key=openai_api_key,
            ai_model=ai_model,
            ai_temperature=ai_temperature,
            enable_ai=enable_ai,
            monitor_groups=monitor_groups,
            auto_detect_transfers=auto_detect_transfers,
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

    def get_ai_api_key(self) -> str:
        """Get the appropriate AI API key based on provider"""
        if self.ai_provider == "mistral":
            if not self.mistral_api_key:
                raise ValueError("MISTRAL_API_KEY environment variable is required when using Mistral AI")
            return self.mistral_api_key
        elif self.ai_provider == "openai":
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required when using OpenAI")
            return self.openai_api_key
        else:
            raise ValueError(f"Unknown AI provider: {self.ai_provider}")
