"""Group message handlers for auto-detection"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.services.ai_service import AIService
from bot.services.balance_service import BalanceService
from bot.services.user_service import UserService

logger = logging.getLogger(__name__)


class GroupHandlers:
    """Handles group messages and auto-detects transfers"""
    
    def __init__(
        self,
        ai_service: AIService,
        balance_service: BalanceService,
        user_service: UserService
    ):
        self.ai_service = ai_service
        self.balance_service = balance_service
        self.user_service = user_service
    
    async def handle_group_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Monitor group messages for transfer announcements"""
        # Only process text messages in groups
        if not update.message or not update.message.text:
            return
        
        if update.effective_chat.type not in ['group', 'supergroup']:
            return
        
        message_text = update.message.text
        sender = update.effective_user
        
        # Skip bot messages
        if sender.is_bot:
            return
        
        logger.info(f"Processing group message from {sender.username or sender.first_name}: {message_text[:50]}...")
        
        # Ensure sender exists in database
        sender_user = self.user_service.get_or_create_user(
            telegram_user_id=sender.id,
            username=sender.username,
            first_name=sender.first_name,
            last_name=sender.last_name
        )
        
        # Detect if this is a transfer announcement
        detection = self.ai_service.detect_transfer(
            message=message_text,
            sender_username=sender.username,
            sender_first_name=sender.first_name
        )
        
        # Only process if high confidence transfer detected
        if not detection.is_transfer or detection.confidence < 0.7:
            logger.debug(f"Not a transfer (confidence: {detection.confidence:.2f})")
            return
        
        logger.info(f"Transfer detected! From: {detection.from_username}, To: {detection.to_username}, Amount: {detection.amount}")
        
        # Validate we have all required information
        if not detection.to_username or not detection.amount:
            logger.warning(f"Missing details - to_username: {detection.to_username}, amount: {detection.amount}")
            await update.message.reply_text(
                "⚠️ I detected a transfer but couldn't extract all details. "
                "Please mention the recipient clearly and specify the amount.\n"
                "Example: 'I transferred $100 to @username'"
            )
            return
        
        # Get or create receiver
        logger.info(f"Looking for receiver: {detection.to_username}")
        receiver_user = self.user_service.get_by_username(detection.to_username)
        
        if not receiver_user:
            # List available users for debugging
            all_users = self.user_service.get_all()
            user_list = ", ".join([f"@{u.username or u.first_name}" for u in all_users])
            logger.warning(f"User '{detection.to_username}' not found. Available users: {user_list}")
            
            await update.message.reply_text(
                f"❌ User '{detection.to_username}' not found in the system.\n\n"
                f"Available users: {user_list}\n\n"
                f"💡 Tip: They need to send at least one message in this group first."
            )
            return
        
        # Prevent self-transfer
        if sender_user.id == receiver_user.id:
            await update.message.reply_text(
                "❌ You cannot transfer money to yourself!"
            )
            return
        
        # Execute the transfer
        result = self.balance_service.transfer_by_user_id(
            from_user_id=sender_user.id,
            to_user_id=receiver_user.id,
            amount=detection.amount,
            message_id=update.message.message_id,
            group_id=update.effective_chat.id
        )
        
        if result.success:
            # Generate AI confirmation message
            confirmation = self.ai_service.generate_confirmation_message(
                from_user_display=sender_user.display_name,
                to_user_display=receiver_user.display_name,
                amount=detection.amount,
                from_balance=sender_user.balance - detection.amount,
                to_balance=receiver_user.balance + detection.amount
            )
            
            await update.message.reply_text(confirmation)
            logger.info(f"Transfer completed: {sender_user.display_name} -> {receiver_user.display_name}, ${detection.amount:.2f}")
        else:
            await update.message.reply_text(result.message)
    
    async def show_my_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show balance for the user who sent the command"""
        user = update.effective_user
        
        # Get or create user
        db_user = self.user_service.get_or_create_user(
            telegram_user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        await update.message.reply_text(
            f"💰 Your Balance\n\n"
            f"{db_user.display_name}: ${db_user.balance:.2f}"
        )
    
    async def show_all_balances(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show balances for all group members"""
        users = self.user_service.get_all()
        
        if not users:
            await update.message.reply_text("No users found in the system yet.")
            return
        
        # Sort by balance descending
        users.sort(key=lambda u: u.balance, reverse=True)
        
        message = "💰 Group Balances\n\n"
        total = 0
        
        for i, user in enumerate(users, 1):
            message += f"{i}. {user.display_name}: ${user.balance:.2f}\n"
            total += user.balance
        
        message += f"\n📊 Total: ${total:.2f}"
        message += f"\n👥 Members: {len(users)}"
        
        await update.message.reply_text(message)
    
    async def show_users(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show all registered users"""
        users = self.user_service.get_all()
        
        if not users:
            await update.message.reply_text("No users registered yet.")
            return
        
        message = "👥 Registered Users:\n\n"
        for i, user in enumerate(users, 1):
            message += f"{i}. {user.display_name}\n"
        
        message += f"\n💡 Total: {len(users)} users"
        await update.message.reply_text(message)
    
    async def show_group_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show recent transactions in the group"""
        history_text = self.balance_service.get_transaction_history(limit=10)
        await update.message.reply_text(history_text)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help message"""
        help_text = (
            "🤖 *Balance Transfer Bot*\n\n"
            "*How it works:*\n"
            "Just announce your transfer naturally:\n"
            "• 'I transferred $100 to @alice'\n"
            "• 'Sent $50 to @bob'\n"
            "• '@charlie I sent you $75'\n\n"
            "*Commands:*\n"
            "/mybalance - Check your balance\n"
            "/balances - See all group balances\n"
            "/users - See registered users\n"
            "/history - View recent transfers\n"
            "/help - Show this message\n\n"
            "*Features:*\n"
            "✅ Auto-detects transfers\n"
            "✅ Updates balances instantly\n"
            "✅ AI-powered understanding\n"
            "✅ Each member starts with $1000\n\n"
            "*⚠️ IMPORTANT:*\n"
            "If bot doesn't respond to messages:\n"
            "1. Message @BotFather\n"
            "2. /mybots → Select bot\n"
            "3. Bot Settings → Group Privacy → Turn OFF\n"
            "4. Remove and re-add bot to group\n\n"
            "*Note:* New members get $1000 automatically!"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')
