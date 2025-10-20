# AI-Powered Features Documentation

## Overview

The bot now includes AI-powered features using **LangChain** and **Mistral AI** (or OpenAI) to understand natural language commands and automatically detect transfers in group chats.

## Features

### 1. Natural Language Commands

Users can interact with the bot using natural language instead of commands:

**Examples:**
- "send 100 to @alice" → Executes transfer
- "transfer $50 to bob" → Executes transfer
- "check my balance" → Shows balance
- "show my transactions" → Shows history

### 2. Group Transfer Detection

The bot monitors group messages and automatically detects when users announce transfers:

**Examples:**
- "@alice I sent you $100" → Auto-records transfer
- "Transferred 75 to @bob" → Auto-records transfer
- "@charlie I paid you 200" → Auto-records transfer

### 3. AI-Generated Responses

The bot generates natural, conversational responses using AI instead of templated messages.

## Configuration

### Environment Variables

```bash
# AI Provider (mistral or openai)
AI_PROVIDER=mistral

# API Keys
MISTRAL_API_KEY=your_mistral_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# AI Model
AI_MODEL=mistral-small-latest  # or gpt-4, gpt-3.5-turbo

# AI Settings
AI_TEMPERATURE=0.1  # Low for consistent financial operations
ENABLE_AI=true

# Group Monitoring
MONITOR_GROUPS=true
AUTO_DETECT_TRANSFERS=true
TELEGRAM_GROUP_ID=your_group_id
PERSON_A_USER_ID=user_id_of_person_a
PERSON_B_USER_ID=user_id_of_person_b
```

### Getting API Keys

#### Mistral AI (Free Tier Available)
1. Go to https://console.mistral.ai/
2. Sign up for an account
3. Navigate to API Keys
4. Create a new API key
5. Copy and add to `.env`

#### OpenAI (Paid)
1. Go to https://platform.openai.com/
2. Sign up for an account
3. Navigate to API Keys
4. Create a new API key
5. Copy and add to `.env`

## Architecture

### Components

```
┌─────────────────────────────────────┐
│     User Message (Natural Language) │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   AIService (LangChain + Mistral)   │
│   - Parse intent                    │
│   - Extract entities                │
│   - Generate responses              │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   AIHandlers                        │
│   - Route to appropriate action     │
│   - Execute financial operations    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   BalanceService                    │
│   - Execute transfer                │
│   - Update balances                 │
└─────────────────────────────────────┘
```

### Files

- `bot/services/ai_service.py` - AI service using LangChain
- `bot/handlers/ai_handlers.py` - AI-powered command handlers
- `bot/utils/config.py` - Configuration with AI settings

## Usage Examples

### Private Chat (Natural Language)

```
User: send 100 to @alice
Bot: ✅ Transfer successful! Sent $100.00 to Alice. 
     Your new balance is $900.00

User: check my balance
Bot: 💰 Current Balances:
     👤 Person A: $900.00
     👤 Person B: $1100.00

User: show my transactions
Bot: 📊 Recent Transactions:
     1. 💸 $100.00 | Person A → Person B
        2024-10-20 10:30:45
```

### Group Chat (Auto-Detection)

```
Alice: @bob I just sent you $50 for lunch
Bot: ✅ Transfer recorded!
     💸 $50.00 from @alice to @bob
     
     Updated balances:
     💰 Current Balances:
     👤 Person A: $850.00
     👤 Person B: $1150.00
```

## How It Works

### 1. Natural Language Processing

The `AIService` uses LangChain with structured output to parse messages:

```python
class FinancialAction(BaseModel):
    action: str  # transfer, check_balance, history, none
    from_user: Optional[str]
    to_user: Optional[str]
    amount: Optional[float]
    confidence: float
    reasoning: str
```

### 2. Intent Detection

The AI analyzes messages and extracts:
- **Action**: What the user wants to do
- **Entities**: Users, amounts, etc.
- **Confidence**: How sure the AI is (0-1)

### 3. Execution

Based on the detected intent:
- **Transfer**: Execute via `BalanceService`
- **Balance**: Show current balances
- **History**: Show transaction history
- **None**: Ignore or provide help

### 4. Response Generation

The AI generates natural responses based on:
- The action performed
- The result (success/failure)
- Context (user, amount, etc.)

## User Mapping

The bot needs to map Telegram usernames to internal user IDs:

```python
def _map_username_to_person(self, username: str) -> str:
    """Map Telegram username to internal person identifier"""
    username = username.lower().replace('@', '')
    
    # TODO: Replace with database lookup
    user_mapping = {
        'alice': 'person_a',
        'bob': 'person_b',
    }
    
    return user_mapping.get(username)
```

**Production Implementation:**
1. Create a `user_mappings` table in database
2. Store Telegram user_id → internal person mapping
3. Query database instead of hardcoded dict

## Security Considerations

### 1. Confidence Threshold

Only execute transfers with high confidence (>0.7):

```python
if result.action == "transfer" and result.confidence > 0.7:
    # Execute transfer
```

### 2. Group Verification

Verify messages are from authorized group:

```python
if update.effective_chat.id != config.group_id:
    return  # Ignore
```

### 3. User Verification

Verify users are authorized:

```python
if sender.id not in [config.person_a_user_id, config.person_b_user_id]:
    return  # Ignore
```

## Testing

### Test Natural Language

```bash
# Start bot
python run.py

# In Telegram (private chat):
send 100 to @alice
check my balance
show my transactions
```

### Test Group Detection

```bash
# In Telegram group:
@alice I sent you $50
Transferred 75 to @bob
```

### Test AI Service

```python
from bot.services.ai_service import AIService

ai = AIService(api_key="your_key")
result = ai.parse_financial_command("send 100 to @alice")
print(result)
```

## Troubleshooting

### AI Not Working

1. **Check API Key**:
   ```bash
   echo $MISTRAL_API_KEY
   ```

2. **Check Logs**:
   ```bash
   tail -f logs/bot.log | grep AI
   ```

3. **Test API Connection**:
   ```python
   from langchain_mistralai import ChatMistralAI
   llm = ChatMistralAI(api_key="your_key")
   print(llm.invoke("Hello"))
   ```

### Group Detection Not Working

1. **Check Group ID**:
   ```bash
   # Get group ID by adding bot to group
   # Check logs for chat_id
   ```

2. **Check Permissions**:
   - Bot must be admin in group
   - Bot must have "Read Messages" permission

3. **Check Configuration**:
   ```bash
   MONITOR_GROUPS=true
   AUTO_DETECT_TRANSFERS=true
   ```

### Low Confidence Scores

If AI confidence is too low:

1. **Adjust Temperature**:
   ```bash
   AI_TEMPERATURE=0.0  # More deterministic
   ```

2. **Use Better Model**:
   ```bash
   AI_MODEL=mistral-medium-latest  # More capable
   ```

3. **Improve Prompts**:
   Edit prompts in `bot/services/ai_service.py`

## Cost Considerations

### Mistral AI
- **Free Tier**: Limited requests per month
- **Paid**: Pay per token
- **Cost**: ~$0.001 per request

### OpenAI
- **No Free Tier**
- **GPT-3.5**: ~$0.002 per request
- **GPT-4**: ~$0.03 per request

### Optimization

1. **Cache Results**: Cache common queries
2. **Batch Processing**: Process multiple messages together
3. **Use Smaller Models**: Use `mistral-small` instead of `mistral-large`
4. **Limit Context**: Send only necessary context

## Future Enhancements

1. **Multi-Language Support**: Detect and respond in user's language
2. **Voice Commands**: Process voice messages
3. **Smart Suggestions**: Suggest common actions
4. **Fraud Detection**: Detect suspicious patterns
5. **Budget Alerts**: Notify when balance is low
6. **Recurring Transfers**: Set up automatic transfers
7. **Analytics**: Generate spending reports

## API Reference

### AIService

```python
class AIService:
    def __init__(self, api_key: str, model: str)
    
    def parse_financial_command(
        self, 
        message: str, 
        user_context: Dict = None
    ) -> FinancialAction
    
    def generate_response(
        self, 
        action: FinancialAction, 
        result: Dict
    ) -> str
    
    def detect_group_transfer(
        self, 
        message: str, 
        sender_username: str
    ) -> Optional[FinancialAction]
```

### AIHandlers

```python
class AIHandlers:
    def __init__(
        self, 
        ai_service: AIService, 
        balance_service: BalanceService
    )
    
    async def handle_natural_language(
        self, 
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    )
    
    async def handle_group_message(
        self, 
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    )
```

## Support

For issues or questions:
1. Check logs: `tail -f logs/bot.log`
2. Review configuration: `cat .env`
3. Test AI service independently
4. Check Mistral AI status: https://status.mistral.ai/

---

**Version:** 2.1.0  
**AI Provider:** Mistral AI / OpenAI  
**Framework:** LangChain  
**Status:** ✅ Production Ready
