# Group Balance Bot - Complete Guide

## 🎯 Overview

This bot manages balances for all members of a Telegram group. When someone announces a transfer, the bot automatically detects it and updates balances.

## ✨ Key Features

- 🤖 **Auto-Detection**: Understands natural language transfer announcements
- 👥 **Multi-User**: Supports unlimited group members
- 💰 **Auto-Registration**: New members get $1000 automatically
- 🔄 **Real-Time Updates**: Balances update instantly
- 🧠 **AI-Powered**: Uses Mistral AI for intelligent detection
- 📊 **Transaction History**: Complete audit trail

## 🚀 Quick Setup

### Step 1: Get API Keys

**A. Telegram Bot Token**
1. Message `@BotFather` on Telegram
2. Send `/newbot`
3. Follow prompts
4. Copy token

**B. Mistral AI Key** (Free!)
1. Visit https://console.mistral.ai/
2. Sign up
3. Create API key
4. Copy key

### Step 2: Configure

Edit `.env`:
```bash
TELEGRAM_BOT_TOKEN=your_telegram_token
MISTRAL_API_KEY=your_mistral_key
AI_PROVIDER=mistral
ENABLE_AI=true
DEFAULT_BALANCE=1000.0
```

### Step 3: Install & Run

```bash
# Install dependencies
./fix_dependencies.sh

# Run bot
python run.py
```

### Step 4: Add to Group

1. Add bot to your Telegram group
2. Make bot an **admin** (required to read messages)
3. Done! Bot is now monitoring

## 💬 How to Use

### Transfer Money

Just announce your transfer naturally in the group:

```
✅ "I transferred $100 to @alice"
✅ "Sent $50 to @bob"
✅ "@charlie I sent you $75"
✅ "I paid @dave $200"
✅ "Transferred $150 to @eve"
```

The bot will:
1. Detect the transfer
2. Verify both users exist
3. Check sender has sufficient balance
4. Update both balances
5. Confirm with a message

### Check Your Balance

```
/mybalance
```

Response:
```
💰 Your Balance

@alice: $900.00
```

### See All Balances

```
/balances
```

Response:
```
💰 Group Balances

1. @bob: $1150.00
2. @alice: $900.00
3. @charlie: $1025.00

📊 Total: $3075.00
👥 Members: 3
```

### View History

```
/history
```

Response:
```
📊 Recent Transactions (Last 10):

1. 💸 $100.00 | @alice → @bob
   2024-10-20 10:30:45

2. 💸 $50.00 | @bob → @charlie
   2024-10-20 10:25:30
```

### Get Help

```
/help
```

## 🎓 Examples

### Example 1: Simple Transfer

```
Alice: I transferred $100 to @bob
Bot: ✅ Transfer recorded!
     💸 $100.00 from @alice to @bob
     
     Updated balances:
     • @alice: $900.00
     • @bob: $1100.00
```

### Example 2: Multiple Transfers

```
Bob: Sent $50 to @charlie
Bot: ✅ Transfer recorded!
     💸 $50.00 from @bob to @charlie
     
     Updated balances:
     • @bob: $1050.00
     • @charlie: $1050.00

Charlie: @alice I sent you $25
Bot: ✅ Transfer recorded!
     💸 $25.00 from @charlie to @alice
     
     Updated balances:
     • @charlie: $1025.00
     • @alice: $925.00
```

### Example 3: Insufficient Funds

```
Dave: I transferred $2000 to @alice
Bot: ❌ Insufficient funds! @dave has $1000.00
```

### Example 4: New Member

```
Eve: (joins group and sends any message)
Bot: (automatically creates account with $1000)

Eve: I sent $100 to @alice
Bot: ✅ Transfer recorded!
     💸 $100.00 from @eve to @alice
```

## 🔧 Configuration

### Environment Variables

```bash
# Required
TELEGRAM_BOT_TOKEN=your_token
MISTRAL_API_KEY=your_key

# Optional
AI_PROVIDER=mistral              # or openai
AI_MODEL=mistral-small-latest    # AI model
ENABLE_AI=true                   # Enable AI features
DEFAULT_BALANCE=1000.0           # Starting balance
DATABASE_URL=data/bot.db         # Database path
LOG_LEVEL=INFO                   # Logging level
```

### Customization

**Change Default Balance:**
```bash
DEFAULT_BALANCE=5000.0  # Everyone starts with $5000
```

**Use OpenAI Instead:**
```bash
AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_key
AI_MODEL=gpt-4
```

## 🧠 How AI Detection Works

The bot uses Mistral AI to understand natural language:

### What It Detects

✅ **Past tense transfers:**
- "I transferred $X to @user"
- "I sent $X to @user"
- "I paid @user $X"

✅ **Various formats:**
- "$100", "100", "$100.50"
- "@username" or "username"

❌ **What it ignores:**
- Questions: "Should I send $100?"
- Future: "I will send $100"
- Requests: "Please send me $100"
- General chat

### Confidence Scoring

- **0.9-1.0**: Clear transfer, all details present
- **0.7-0.9**: Likely transfer, some ambiguity
- **0.5-0.7**: Possible transfer, unclear
- **< 0.7**: Ignored (not processed)

## 📊 Database Schema

### Users Table
```sql
- id (PRIMARY KEY)
- telegram_user_id (UNIQUE)
- username
- first_name
- last_name
- balance
- created_at
- updated_at
```

### Transactions Table
```sql
- id (PRIMARY KEY)
- from_user_id (FOREIGN KEY)
- to_user_id (FOREIGN KEY)
- amount
- balance_from
- balance_to
- message_id
- group_id
- created_at
```

## 🔒 Security

### Permissions Required

Bot needs to be **admin** in the group to:
- Read all messages
- Detect transfer announcements
- Reply to messages

### Data Privacy

- Only stores: user ID, username, balance
- No message content stored
- Transactions logged for audit
- Database stored locally

### Validation

- ✅ Amount must be positive
- ✅ Sender must have sufficient balance
- ✅ Cannot transfer to yourself
- ✅ Both users must exist
- ✅ High confidence required (>0.7)

## 🐛 Troubleshooting

### Bot Doesn't Detect Transfers

**Check:**
1. Bot is admin in group
2. AI is enabled: `ENABLE_AI=true`
3. API key is valid
4. Message format is clear

**Test:**
```
# Clear format
I transferred $100 to @alice

# Not clear
maybe send 100 to alice?
```

### User Not Found

**Solution:**
User needs to send at least one message in the group first. This creates their account.

### Balance Not Updating

**Check logs:**
```bash
tail -f logs/bot.log
```

Look for:
- Transfer detection
- Confidence score
- Error messages

### AI Not Working

**Verify installation:**
```bash
python -c "from langchain_mistralai import ChatMistralAI; print('OK')"
```

**Check API key:**
```bash
echo $MISTRAL_API_KEY
```

## 💡 Tips

1. **Be Clear**: Use clear transfer statements
2. **Use @mentions**: Always mention receiver with @
3. **Specify Amount**: Include $ or number clearly
4. **Past Tense**: Say "I transferred" not "I will transfer"
5. **Check Balance**: Use `/mybalance` before large transfers

## 📈 Scaling

### Current Capacity
- Unlimited users
- Unlimited transactions
- SQLite database
- Suitable for groups up to 1000 members

### For Larger Groups
- Switch to PostgreSQL
- Add caching layer
- Implement rate limiting
- Add backup system

## 🎯 Use Cases

### 1. Friend Groups
Track who owes what for shared expenses

### 2. Team Budgets
Manage team spending and transfers

### 3. Gaming Communities
Virtual currency for games

### 4. Study Groups
Track shared resource costs

### 5. Family Groups
Manage family finances

## 🔄 Workflow

```
1. User joins group
   ↓
2. Bot creates account ($1000)
   ↓
3. User announces transfer
   ↓
4. AI detects transfer
   ↓
5. Bot validates
   ↓
6. Balances updated
   ↓
7. Confirmation sent
```

## 📞 Support

**Check logs:**
```bash
tail -f logs/bot.log
```

**Verify database:**
```bash
sqlite3 data/bot.db
SELECT * FROM users;
SELECT * FROM transactions;
```

**Test AI:**
```bash
python -c "from bot.services.ai_service import AIService; print('OK')"
```

## 🎉 Success Checklist

- [ ] Bot token obtained
- [ ] Mistral AI key obtained
- [ ] Dependencies installed
- [ ] `.env` configured
- [ ] Bot running
- [ ] Bot added to group
- [ ] Bot is admin
- [ ] Test transfer works
- [ ] Balances update correctly

## 🚀 Next Steps

1. **Add bot to your group**
2. **Make it admin**
3. **Test with a transfer**
4. **Invite members**
5. **Start tracking!**

---

**Version:** 2.1.0  
**AI:** Mistral AI  
**Database:** SQLite  
**Status:** ✅ Production Ready

**Ready to use!** Add the bot to your group and start tracking transfers! 🎉
