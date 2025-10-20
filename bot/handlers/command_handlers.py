"""Telegram bot command handlers"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from bot.services.balance_service import BalanceService

logger = logging.getLogger(__name__)


class CommandHandlers:
    """Handles all bot commands and callbacks"""
    
    # Conversation states
    TRANSFER_AMOUNT = 1
    
    def __init__(self, balance_service: BalanceService):
        self.balance_service = balance_service
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        welcome_message = (
            "👋 Welcome to the Balance Transfer Bot v2.0!\n\n"
            "🔹 Now powered by SQLite database\n"
            "🔹 Scalable architecture\n"
            "🔹 Enhanced performance\n\n"
            "Available commands:\n"
            "💰 /balance - Check current balances\n"
            "💸 /transfer - Transfer money between users\n"
            "🔄 /reset - Reset balances to default\n"
            "📊 /history - View recent transactions\n"
            "📈 /stats - View statistics\n"
            "❓ /help - Show detailed help"
        )
        await update.message.reply_text(welcome_message)
        logger.info(f"User {update.effective_user.id} started the bot")
    
    async def show_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show current balances"""
        balance_text = self.balance_service.get_all_balances()
        await update.message.reply_text(balance_text)
        logger.info(f"User {update.effective_user.id} checked balances")
    
    async def transfer_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start transfer process - select direction"""
        keyboard = [
            [InlineKeyboardButton("Person A → Person B", callback_data='transfer_a_to_b')],
            [InlineKeyboardButton("Person B → Person A", callback_data='transfer_b_to_a')],
            [InlineKeyboardButton("❌ Cancel", callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Select transfer direction:",
            reply_markup=reply_markup
        )
        
        return self.TRANSFER_AMOUNT
    
    async def transfer_direction(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle transfer direction selection"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'cancel':
            await query.edit_message_text("❌ Transfer cancelled.")
            return ConversationHandler.END
        
        # Store transfer direction in context
        if query.data == 'transfer_a_to_b':
            context.user_data['from'] = 'person_a'
            context.user_data['to'] = 'person_b'
            direction_text = "Person A → Person B"
        else:
            context.user_data['from'] = 'person_b'
            context.user_data['to'] = 'person_a'
            direction_text = "Person B → Person A"
        
        from_balance = self.balance_service.get_balance(context.user_data['from'])
        
        await query.edit_message_text(
            f"💸 Transfer: {direction_text}\n\n"
            f"Available balance: ${from_balance:.2f}\n\n"
            f"Please enter the amount to transfer:\n"
            f"(Type a number or /cancel to cancel)"
        )
        
        logger.info(
            f"User {update.effective_user.id} selected transfer: "
            f"{context.user_data['from']} -> {context.user_data['to']}"
        )
        
        return self.TRANSFER_AMOUNT
    
    async def transfer_amount(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process transfer amount"""
        try:
            amount = float(update.message.text.strip())
            
            from_person = context.user_data.get('from')
            to_person = context.user_data.get('to')
            
            if not from_person or not to_person:
                await update.message.reply_text(
                    "❌ Transfer session expired. Please start again with /transfer"
                )
                return ConversationHandler.END
            
            result = self.balance_service.transfer(from_person, to_person, amount)
            
            if result.success:
                balance_text = self.balance_service.get_all_balances()
                await update.message.reply_text(f"{result.message}\n\n{balance_text}")
                logger.info(
                    f"User {update.effective_user.id} completed transfer: "
                    f"{from_person} -> {to_person}, ${amount:.2f}"
                )
            else:
                await update.message.reply_text(result.message)
            
        except ValueError:
            await update.message.reply_text(
                "❌ Invalid amount! Please enter a valid number.\n"
                "Example: 50 or 123.45"
            )
            return self.TRANSFER_AMOUNT
        
        # Clear user data
        context.user_data.clear()
        return ConversationHandler.END
    
    async def cancel_transfer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel the transfer"""
        await update.message.reply_text("❌ Transfer cancelled.")
        context.user_data.clear()
        logger.info(f"User {update.effective_user.id} cancelled transfer")
        return ConversationHandler.END
    
    async def reset_balances(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Reset balances to default"""
        keyboard = [
            [InlineKeyboardButton("✅ Yes, Reset", callback_data='confirm_reset')],
            [InlineKeyboardButton("❌ Cancel", callback_data='cancel_reset')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "⚠️ Are you sure you want to reset all balances to default?\n"
            "This will clear all transaction history.",
            reply_markup=reply_markup
        )
    
    async def confirm_reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Confirm reset action"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'confirm_reset':
            self.balance_service.reset_all_balances()
            balance_text = self.balance_service.get_all_balances()
            await query.edit_message_text(f"✅ Balances reset!\n\n{balance_text}")
            logger.info(f"User {update.effective_user.id} reset all balances")
        else:
            await query.edit_message_text("❌ Reset cancelled.")
    
    async def show_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show transaction history"""
        history_text = self.balance_service.get_transaction_history()
        await update.message.reply_text(history_text)
        logger.info(f"User {update.effective_user.id} viewed transaction history")
    
    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show statistics"""
        total_transactions = self.balance_service.transaction_service.get_count()
        users = self.balance_service.user_service.get_all()
        
        stats_text = (
            "📈 *Bot Statistics*\n\n"
            f"👥 Total Users: {len(users)}\n"
            f"💸 Total Transactions: {total_transactions}\n\n"
            "💾 Database: SQLite\n"
            "🏗️ Architecture: Scalable\n"
            "📦 Version: 2.0.0"
        )
        await update.message.reply_text(stats_text, parse_mode='Markdown')
        logger.info(f"User {update.effective_user.id} viewed statistics")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help message"""
        help_text = (
            "📖 *Balance Transfer Bot Help*\n\n"
            "*Commands:*\n"
            "💰 /balance - View current balances of all users\n"
            "💸 /transfer - Initiate a transfer between users\n"
            "🔄 /reset - Reset all balances to default\n"
            "📊 /history - View recent transaction history\n"
            "📈 /stats - View bot statistics\n"
            "❓ /help - Display this help message\n\n"
            "*How to Transfer:*\n"
            "1. Use /transfer command\n"
            "2. Select transfer direction\n"
            "3. Enter the amount\n"
            "4. Confirm the transfer\n\n"
            "*Features:*\n"
            "✅ SQLite database storage\n"
            "✅ Real-time balance updates\n"
            "✅ Insufficient funds protection\n"
            "✅ Complete transaction history\n"
            "✅ Scalable architecture\n"
            "✅ Easy-to-use interface\n\n"
            "*Version:* 2.0.0"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred while processing your request. "
                "Please try again or contact support."
            )
