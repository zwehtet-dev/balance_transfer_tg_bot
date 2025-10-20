"""AI Service using LangChain and Mistral AI - Latest Patterns"""

import logging
import json
from typing import Dict, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# Try to import LangChain dependencies
try:
    from langchain_mistralai import ChatMistralAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import PydanticOutputParser
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    logger.warning(f"LangChain not available: {e}")
    logger.warning("AI features will be disabled. Install with: pip install langchain langchain-mistralai")
    LANGCHAIN_AVAILABLE = False


class TransferDetection(BaseModel):
    """Structured output for transfer detection"""
    is_transfer: bool = Field(description="Whether this message describes a money transfer")
    from_username: Optional[str] = Field(default=None, description="Username of sender (without @)")
    to_username: Optional[str] = Field(default=None, description="Username of receiver (without @)")
    amount: Optional[float] = Field(default=None, description="Amount transferred")
    confidence: float = Field(description="Confidence score 0-1")
    reasoning: str = Field(description="Explanation of the decision")


class AIService:
    """Service for AI-powered transfer detection in group chats"""
    
    def __init__(self, api_key: str, model: str = "mistral-small-latest"):
        if not LANGCHAIN_AVAILABLE:
            raise ImportError(
                "LangChain is not installed. Install with: "
                "pip install langchain langchain-mistralai"
            )
        
        self.api_key = api_key
        self.model = model
        self.llm = ChatMistralAI(
            api_key=api_key,
            model=model,
            temperature=0.0  # Deterministic for financial operations
        )
        logger.info(f"Initialized Mistral AI with model: {model}")
    
    def detect_transfer(
        self,
        message: str,
        sender_username: str = None,
        sender_first_name: str = None
    ) -> TransferDetection:
        """
        Detect if a message describes a money transfer
        
        Args:
            message: The message text
            sender_username: Username of message sender
            sender_first_name: First name of sender
        
        Returns:
            TransferDetection with parsed information
        """
        parser = PydanticOutputParser(pydantic_object=TransferDetection)
        
        # Build context about sender
        sender_info = sender_username or sender_first_name or "Unknown"
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a financial transaction detector for a Telegram group.

Your job is to detect when someone announces they have transferred money to another person.

IMPORTANT RULES:
1. Only detect PAST transfers (already completed)
2. Look for patterns like:
   - "I transferred $X to @user"
   - "I sent $X to @user"
   - "I paid @user $X"
   - "Sent $X to @user"
   - "@user I sent you $X"
   
3. Extract:
   - from_username: The sender (usually the message author)
   - to_username: The receiver (mentioned with @ or by name)
   - amount: The money amount (can be $100, 100, $100.50, etc.)

4. DO NOT detect:
   - Questions ("should I send?")
   - Future plans ("I will send")
   - Requests ("please send me")
   - General chat

5. Confidence scoring:
   - 0.9-1.0: Clear transfer statement with all details
   - 0.7-0.9: Likely transfer but some ambiguity
   - 0.5-0.7: Possible transfer but unclear
   - 0.0-0.5: Not a transfer

Message sender: {sender}

{format_instructions}"""),
            ("user", "Message: {message}")
        ])
        
        chain = prompt | self.llm | parser
        
        try:
            result = chain.invoke({
                "message": message,
                "sender": sender_info,
                "format_instructions": parser.get_format_instructions()
            })
            
            logger.info(
                f"Transfer detection: is_transfer={result.is_transfer}, "
                f"confidence={result.confidence:.2f}, "
                f"from={result.from_username}, to={result.to_username}, "
                f"amount={result.amount}"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error detecting transfer: {e}", exc_info=True)
            # Return safe default
            return TransferDetection(
                is_transfer=False,
                confidence=0.0,
                reasoning=f"Error: {str(e)}"
            )
    
    def generate_confirmation_message(
        self,
        from_user_display: str,
        to_user_display: str,
        amount: float,
        from_balance: float,
        to_balance: float
    ) -> str:
        """Generate a natural confirmation message"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a friendly financial bot assistant.
            
Generate a brief, natural confirmation message for a completed transfer.

Guidelines:
- Be concise (1-2 sentences)
- Use emojis appropriately
- Confirm the transfer
- Show updated balances
- Be professional but friendly"""),
            ("user", """Transfer completed:
From: {from_user}
To: {to_user}
Amount: ${amount:.2f}
New balance for {from_user}: ${from_balance:.2f}
New balance for {to_user}: ${to_balance:.2f}

Generate confirmation message:""")
        ])
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({
                "from_user": from_user_display,
                "to_user": to_user_display,
                "amount": amount,
                "from_balance": from_balance,
                "to_balance": to_balance
            })
            return response.content
        except Exception as e:
            logger.error(f"Error generating message: {e}")
            # Fallback to template
            return (
                f"✅ Transfer recorded!\n"
                f"💸 ${amount:.2f} from {from_user_display} to {to_user_display}\n\n"
                f"Updated balances:\n"
                f"• {from_user_display}: ${from_balance:.2f}\n"
                f"• {to_user_display}: ${to_balance:.2f}"
            )
