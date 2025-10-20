# Complete Setup Guide - AI-Powered Telegram Bot

## 🎯 What You're Building

A Telegram bot that:
- ✅ Manages balances for Person A and Person B
- ✅ Handles transfers with auto-update
- ✅ Understands natural language ("send 100 to @alice")
- ✅ Auto-detects transfers in group chats
- ✅ Uses AI (Mistral AI) for intelligent responses

## 📋 Prerequisites

- Python 3.8 or higher
- Telegram account
- Mistral AI account (free tier available)

## 🚀 Quick Setup (5 Minutes)

### Step 1: Get Your Tokens

#### A. Telegram Bot Token
1. Open Telegram, search for `@BotFather`
2. Send `/newbot`
3. Follow prompts to create your bot
4. Copy the token (looks like: `123456789:ABCdef...`)

#### B. Mistral AI API Key (Free!)
1. Visit https://console.mistral.ai/
2. Sign up for free account
3. Go to "API Keys"
4. Create new key
5. Copy the key

### Step 2: Install Dependencies

**Option A: Automated (Recommended)**
```bash
chmod +x fix_dependencies.sh
./fix_dependencies.sh
```

**Option B: Manual**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install
pip install --upgrade pip
pip install python-telegram-bot==20.7 python-dotenv==1.0.0
pip install langchain==0.1.20
pip install langchain-mistralai==0.1.0
```

**Option C: Without AI (if issues)**
```bash
pip install -r requirements-minimal.txt
```

### Step 3: Configure

```bash
# Copy example
cp .env.example .env

# Edit with your tokens
nano .env
```

Add your tokens:
```bash
TELEGRAM_BOT_TOKEN=your_telegram_token_here
MISTRAL_API_KEY=your_mistral_key_here
ENABLE_AI=true
```

### Step 4: Run

```bash
python run.py
```

You should see:
```
INFO - Starting Balance Transfer Bot v2.1.0
INFO - AI service initialized with mistral
INFO - Bot is running! Press Ctrl+C to stop.
```

### Step 5: Test

Open Telegram and message your bot:

**Traditional Commands:**
```
/start
/balance
/transfer
```

**AI-Powered (Natural Language):**
```
send 100 to @alice
check my balance
show my transactions
```

## 🎓 Usage Examples

### Private Chat

```
You: send 100 to @alice
Bot: ✅ Transfer successful! Sent $100.00 to Alice.
     Your new balance is $900.00

You: check my balance
Bot: 💰 Current Balances:
     👤 Person A: $900.00
     👤 Person B: $1100.00

You: show my transactions
Bot: 📊 Recent Transactions:
     1. 💸 $100.00 | Person A → Person B
        2024-10-20 10:30:45
```

### Group Chat (Auto-Detection)

```
Alice: @bob I just sent you $50
Bot: ✅ Transfer recorded!
     💸 $50.00 from @alice to @bob
     
     Updated balances:
     💰 Current Balances:
     👤 Person A: $850.00
     👤 Person B: $1150.00
```

## 🔧 Configuration Options

### Basic Configuration (.env)

```bash
# Required
TELEGRAM_BOT_TOKEN=your_token
MISTRAL_API_KEY=your_key

# Optional
AI_PROVIDER=mistral              # or openai
AI_MODEL=mistral-small-latest    # AI model to use
ENABLE_AI=true                   # Enable AI features
DEFAULT_BALANCE=1000.0           # Starting balance
```

### Group Monitoring (.env)

```bash
MONITOR_GROUPS=true              # Monitor group chats
AUTO_DETECT_TRANSFERS=true       # Auto-detect transfers
TELEGRAM_GROUP_ID=-1001234567890 # Your group ID
```

## 🐛 Troubleshooting

### Issue: Dependency Installation Failed

**Solution:**
```bash
# Use fix script
./fix_dependencies.sh

# Or install minimal version
pip install -r requirements-minimal.txt
# Set ENABLE_AI=false in .env
```

See [DEPENDENCY_FIX.md](DEPENDENCY_FIX.md) for details.

### Issue: Bot Doesn't Respond

**Check:**
1. Bot is running: `ps aux | grep python`
2. Token is correct: `cat .env | grep TOKEN`
3. Logs: `tail -f logs/bot.log`

### Issue: AI Not Working

**Check:**
1. API key is set: `cat .env | grep MISTRAL`
2. AI is enabled: `cat .env | grep ENABLE_AI`
3. Dependencies installed: `pip list | grep langchain`

**Test:**
```python
python -c "from langchain_mistralai import ChatMistralAI; print('OK')"
```

### Issue: Group Detection Not Working

**Setup:**
1. Add bot to group as admin
2. Get group ID from logs
3. Add to `.env`: `TELEGRAM_GROUP_ID=-1001234567890`
4. Restart bot

## 📚 Documentation

- **README.md** - Main documentation
- **AI_FEATURES.md** - AI features in detail
- **SETUP_AI.md** - AI setup guide
- **INSTALL_GUIDE.md** - Installation guide
- **DEPENDENCY_FIX.md** - Fix dependency issues
- **QUICK_REFERENCE.md** - Command reference

## 🎯 What Commands Work?

### Traditional Commands
- `/start` - Welcome message
- `/balance` - Check balances
- `/transfer` - Transfer money
- `/history` - View transactions
- `/stats` - View statistics
- `/reset` - Reset balances
- `/help` - Show help

### Natural Language (AI)
- "send 100 to @alice"
- "transfer $50 to bob"
- "check my balance"
- "show my transactions"
- "what's my balance?"

### Group Auto-Detection
- "@alice I sent you $100"
- "Transferred 75 to @bob"
- "@charlie I paid you 200"

## 💡 Tips

1. **Start Simple**: Test with traditional commands first
2. **Enable AI**: Once working, enable AI features
3. **Monitor Logs**: Check `logs/bot.log` for issues
4. **Test Gradually**: Test private chat, then group
5. **Backup Data**: Database is in `data/bot.db`

## 🚦 Next Steps

1. ✅ Bot running? Test with `/start`
2. ✅ AI working? Test with "send 100 to alice"
3. ✅ Group setup? Add bot to group
4. ✅ Customize? Edit prompts in `bot/services/ai_service.py`

## 📊 Architecture

```
User Message
    ↓
AI Service (Mistral AI + LangChain)
    ├── Understand Intent
    ├── Extract Details
    └── Generate Response
    ↓
Balance Service
    ├── Validate
    ├── Execute Transfer
    └── Update Database (SQLite)
    ↓
Response to User
```

## 💰 Cost

### Mistral AI
- **Free Tier**: Limited requests/month
- **Perfect for**: Testing, small deployments
- **Cost**: ~$0.001 per request (paid tier)

### OpenAI (Alternative)
- **No Free Tier**
- **Cost**: ~$0.002-0.03 per request
- **Setup**: Set `AI_PROVIDER=openai` in `.env`

## 🎉 Success Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed
- [ ] Telegram bot token obtained
- [ ] Mistral AI key obtained
- [ ] `.env` configured
- [ ] Bot running
- [ ] Traditional commands work
- [ ] AI commands work
- [ ] Group detection works (optional)

## 🆘 Getting Help

1. **Check Logs**: `tail -f logs/bot.log`
2. **Verify Config**: `cat .env`
3. **Test Dependencies**: `pip list`
4. **Read Docs**: See documentation files
5. **Try Minimal**: Use `requirements-minimal.txt`

## 🎓 Learning Resources

- **LangChain**: https://python.langchain.com/
- **Mistral AI**: https://docs.mistral.ai/
- **Telegram Bots**: https://core.telegram.org/bots

---

**Ready to start?** Run `./fix_dependencies.sh` and then `python run.py`!

**Questions?** Check the documentation or logs!

**Version:** 2.1.0  
**Status:** ✅ Production Ready  
**AI:** Mistral AI + LangChain
