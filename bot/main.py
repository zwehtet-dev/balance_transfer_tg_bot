"""
Telegram Balance Transfer Bot - Main Entry Point
"""

import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.utils.config import BotConfig
from bot.utils.logger import setup_logging
from bot.services.bot_service import BotService


def main():
    """Main function to run the bot"""
    try:
        # Load configuration
        config = BotConfig.from_env()
        
        # Setup logging
        setup_logging(config)
        logger = logging.getLogger(__name__)
        
        logger.info("=" * 50)
        logger.info("Starting Balance Transfer Bot v2.0.0")
        logger.info("=" * 50)
        logger.info(f"Database: {config.database_url}")
        logger.info(f"Storage: SQLite")
        
        # Create and run bot service
        bot_service = BotService(config)
        bot_service.run()
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nPlease set the TELEGRAM_BOT_TOKEN environment variable.")
        print("Example: export TELEGRAM_BOT_TOKEN='your_token_here'")
        sys.exit(1)
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
