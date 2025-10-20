"""Main bot service"""

import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)
from bot.utils.config import BotConfig
from bot.models.database import Database, init_database
from bot.services.balance_service import BalanceService
from bot.services.user_service import UserService
from bot.services.ai_service import AIService
from bot.handlers.group_handlers import GroupHandlers

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
        self.user_service = UserService(self.db, config.default_balance)
        self.balance_service = BalanceService(self.db, config.default_balance)
        
        # Initialize AI service if enabled
        self.ai_service = None
        self.group_handlers = None
        
        if config.enable_ai:
            try:
                api_key = config.get_ai_api_key()
                self.ai_service = AIService(api_key, config.ai_model)
                self.group_handlers = GroupHandlers(
                    self.ai_service,
                    self.balance_service,
                    self.user_service
                )
                logger.info(f"AI service initialized with {config.ai_provider}")
            except Exception as e:
                logger.warning(f"AI service not available: {e}")
                logger.info("Bot will run without AI features")
        
        self.application = None
    
    def _setup_handlers(self):
        """Setup all command and callback handlers"""
        
        if not self.group_handlers:
            logger.error("Group handlers not initialized! AI features required.")
            return
        
        # Command handlers
        self.application.add_handler(
            CommandHandler("help", self.group_handlers.help_command)
        )
        self.application.add_handler(
            CommandHandler("start", self.group_handlers.help_command)
        )
        self.application.add_handler(
            CommandHandler("mybalance", self.group_handlers.show_my_balance)
        )
        self.application.add_handler(
            CommandHandler("balances", self.group_handlers.show_all_balances)
        )
        self.application.add_handler(
            CommandHandler("users", self.group_handlers.show_users)
        )
        self.application.add_handler(
            CommandHandler("history", self.group_handlers.show_group_history)
        )
        
        # Group message monitoring for auto-detection
        self.application.add_handler(
            MessageHandler(
                filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND,
                self.group_handlers.handle_group_message
            )
        )
        logger.info("Group message monitoring enabled")
        
        # Error handler
        self.application.add_error_handler(self._error_handler)
    
    async def _error_handler(self, update, context):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred. Please try again or contact support."
            )
    
    async def post_init(self, application: Application):
        """Post initialization hook"""
        logger.info("Bot initialized successfully")
        logger.info(f"Database: {self.config.database_url}")
        
        # Log initial state
        user_count = self.user_service.get_user_count()
        logger.info(f"Users in database: {user_count}")
    
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
        
        logger.info("🤖 Bot is running! Add to your group and give admin access.")
        logger.info("📝 Users will be auto-created with $1000 balance")
        logger.info("💬 Bot will auto-detect transfer messages")
        logger.info("Press Ctrl+C to stop.")
        
        self.application.run_polling(
            allowed_updates=["message"],
            drop_pending_updates=True
        )
    
    def stop(self):
        """Stop the bot gracefully"""
        if self.application and self.application.running:
            logger.info("Stopping bot...")
            self.application.stop()
            self.db.close()
