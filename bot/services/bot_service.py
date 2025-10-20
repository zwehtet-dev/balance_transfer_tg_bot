"""Main bot service"""

import logging
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters
)
from bot.utils.config import BotConfig
from bot.models.database import Database, init_database
from bot.services.balance_service import BalanceService
from bot.handlers.command_handlers import CommandHandlers

logger = logging.getLogger(__name__)


class BotService:
    """Main bot service that orchestrates everything"""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.config.ensure_directories()
        
        # Initialize database
        self.db = Database(config.database_url)
        init_database(self.db)
        
        # Initialize services
        self.balance_service = BalanceService(self.db)
        self.handlers = CommandHandlers(self.balance_service)
        self.application = None
    
    def _setup_handlers(self):
        """Setup all command and callback handlers"""
        # Basic command handlers
        self.application.add_handler(CommandHandler("start", self.handlers.start))
        self.application.add_handler(CommandHandler("balance", self.handlers.show_balance))
        self.application.add_handler(CommandHandler("help", self.handlers.help_command))
        self.application.add_handler(CommandHandler("reset", self.handlers.reset_balances))
        self.application.add_handler(CommandHandler("history", self.handlers.show_history))
        self.application.add_handler(CommandHandler("stats", self.handlers.show_stats))
        
        # Transfer conversation handler
        transfer_conv_handler = ConversationHandler(
            entry_points=[CommandHandler("transfer", self.handlers.transfer_start)],
            states={
                CommandHandlers.TRANSFER_AMOUNT: [
                    CallbackQueryHandler(
                        self.handlers.transfer_direction,
                        pattern='^transfer_'
                    ),
                    CallbackQueryHandler(
                        self.handlers.cancel_transfer,
                        pattern='^cancel$'
                    ),
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND,
                        self.handlers.transfer_amount
                    )
                ]
            },
            fallbacks=[CommandHandler("cancel", self.handlers.cancel_transfer)]
        )
        self.application.add_handler(transfer_conv_handler)
        
        # Reset confirmation handler
        self.application.add_handler(
            CallbackQueryHandler(
                self.handlers.confirm_reset,
                pattern='^(confirm_reset|cancel_reset)$'
            )
        )
        
        # Error handler
        self.application.add_error_handler(self.handlers.error_handler)
    
    async def post_init(self, application: Application):
        """Post initialization hook"""
        logger.info("Bot initialized successfully")
        logger.info(f"Database: {self.config.database_url}")
        
        # Log initial state
        users = self.balance_service.user_service.get_all()
        logger.info(f"Loaded {len(users)} users from database")
    
    async def post_shutdown(self, application: Application):
        """Post shutdown hook"""
        logger.info("Shutting down bot...")
        self.db.close()
        logger.info("Bot shutdown complete")
    
    def run(self):
        """Start the bot"""
        logger.info("Initializing bot application...")
        
        self.application = (
            Application.builder()
            .token(self.config.token)
            .post_init(self.post_init)
            .post_shutdown(self.post_shutdown)
            .build()
        )
        
        logger.info("Setting up handlers...")
        self._setup_handlers()
        
        logger.info("Bot is running! Press Ctrl+C to stop.")
        self.application.run_polling(
            allowed_updates=["message", "callback_query"],
            drop_pending_updates=True
        )
    
    def stop(self):
        """Stop the bot gracefully"""
        if self.application and self.application.running:
            logger.info("Stopping bot...")
            self.application.stop()
            self.db.close()
