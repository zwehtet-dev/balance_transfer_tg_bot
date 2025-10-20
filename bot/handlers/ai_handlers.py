"""AI-powered command handlers"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.services.ai_service import AIService
from bot.services.balance_service import BalanceService

logger = logging.getLogger(__name__)


class AIHandlers:
    """Handles AI-powered natural language commands"""
    
    def __init__(self, ai_service: AIService, balance_service: BalanceService):
        self.ai_service = ai_service
        self.balance_service = balance_service
    
    async def handle_natural_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle natural language financial commands"""
        message_text = update.message.text
        user = update.effective_user
        
        # Build context
        user_context = {
            "username": user.username or user.first_name,
            "user_id": user.id,
            "chat_type": update.effective_chat.type
        }
        
        logger.info(f"Processing NL command from {user.username}: {message_text}")
        
        # Parse the command using AI
        action = self.ai_service.parse_financial_command(message_text, user_context)
        
        # Execute based on action
        if action.action == "transfer":
            await self._handle_ai_transfer(update, action)
        elif action.action == "check_balance":
            await self._handle_ai_balance(update)
        elif action.action == "history":
            await self._handle_ai_history(update)
        else:
            # Not a financial command, ignore or provide help
            if action.confidence < 0.3:
                return  # Likely not meant for the bot
            await update.message.reply_text(
                "I'm a financial assistant bot. I can help you with:\n"
                "💸 Transfers: 'send 100 to @user'\n"
                "💰 Balance: 'check my balance'\n"
                "📊 History: 'show my transactions'"
            )
    
    async def _handle_ai_transfer(self, update: Update, action):
        """Handle AI-detected transfer"""
        if not action.to_user or not action.amount:
            await update.message.reply_text(
                "❌ I couldn't understand the transfer details. Please specify:\n"
                "- Who to send to (e.g., @username)\n"
                "- How much to send (e.g., 100)"
            )
            return
        
        # Map usernames to person_a/person_b
        # In production, you'd have a user mapping service
        from_person = self._map_username_to_person(update.effective_user.username)
        to_person = self._map_username_to_person(action.to_user)
        
        if not from_person or not to_person:
            await update.message.reply_text(
                "❌ User not found in the system. Only registered users can transfer."
            )
            return
        
        # Execute transfer
        result = self.balance_service.transfer(from_person, to_person, action.amount)
        
        if result.success:
            # Generate AI response
            response = self.ai_service.generate_response(action, {
                "success": True,
                "amount": action.amount,
                "from": from_person,
                "to": to_person,
                "new_balance": self.balance_service.get_balance(from_person)
            })
            await update.message.reply_text(response)
        else:
            await update.message.reply_text(result.message)
    
    async def _handle_ai_balance(self, update: Update):
        """Handle AI-detected balance check"""
        balance_text = self.balance_service.get_all_balances()
        await update.message.reply_text(balance_text)
    
    async def _handle_ai_history(self, update: Update):
        """Handle AI-detected history request"""
        history_text = self.balance_service.get_transaction_history()
        await update.message.reply_text(history_text)
    
    async def handle_group_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Monitor group messages for transfer announcements"""
        # Only process in groups
        if update.effective_chat.type not in ['group', 'supergroup']:
            return
        
        message_text = update.message.text
        sender = update.effective_user
        
        # Detect if this is a transfer announcement
        action = self.ai_service.detect_group_transfer(message_text, sender.username)
        
        if action and action.action == "transfer":
            logger.info(f"Detected group transfer: {action}")
            
            # Map usernames
            from_person = self._map_username_to_person(action.from_user or sender.username)
            to_person = self._map_username_to_person(action.to_user)
            
            if from_person and to_person and action.amount:
                # Execute transfer
                result = self.balance_service.transfer(from_person, to_person, action.amount)
                
                if result.success:
                    await update.message.reply_text(
                        f"✅ Transfer recorded!\n"
                        f"💸 ${action.amount:.2f} from @{action.from_user} to @{action.to_user}\n\n"
                        f"Updated balances:\n"
                        f"{self.balance_service.get_all_balances()}"
                    )
                else:
                    await update.message.reply_text(
                        f"❌ Could not process transfer: {result.message}"
                    )
    
    def _map_username_to_person(self, username: str) -> str:
        """
        Map Telegram username to internal person identifier
        In production, this would query a user mapping table
        """
        if not username:
            return None
        
        username = username.lower().replace('@', '')
        
        # TODO: Replace with actual user mapping from database
        # For now, simple mapping for demo
        user_mapping = {
            'person_a': 'person_a',
            'person_b': 'person_b',
            'alice': 'person_a',
            'bob': 'person_b',
        }
        
        return user_mapping.get(username)
