"""Logging configuration"""

import logging
import sys
from pathlib import Path
from bot.utils.config import BotConfig


def setup_logging(config: BotConfig):
    """Configure logging for the application"""
    # Ensure log directory exists
    config.ensure_directories()
    
    # Create formatters
    formatter = logging.Formatter(config.log_format)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # File handler
    file_handler = logging.FileHandler(config.log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.log_level.upper()))
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Reduce noise from telegram library
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.WARNING)
    
    logging.info("Logging configured successfully")
