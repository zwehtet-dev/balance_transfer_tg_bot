# Quick Start - Group Balance Bot

## 🚀 Get Running in 5 Minutes!

### Step 1: Get Tokens (2 minutes)

**Telegram Bot:**
1. Message `@BotFather`
2. Send `/newbot`
3. Copy token

**Mistral AI (Free!):**
1. Visit https://console.mistral.ai/
2. Sign up
3. Create API key
4. Copy key

### Step 2: Install (1 minute)

```bash
chmod +x fix_dependencies.sh
./fix_dependencies.sh
```

### Step 3: Configure (1 minute)

Edit `.env`:
```bash
TELEGRAM_BOT_TOKEN=paste_your_telegram_token_here
MISTRAL_API_KEY=paste_your_mistral_key_here
ENABLE_AI=true
```

### Step 4: Run (30 seconds)

```bash
python run.py
```

You should see:
```
INFO - 🤖 Bot is running!
INFO - 📝 Users will be auto-created with $1000 balance
INFO - 💬 Bot will auto-detect transfer messages
```

### Step 5: Add to Group (30 seconds)

1. Add bot to your Telegram group
2. Go to group settings → Administrators
3. Add bot as admin
4. Done!

## ✅ Test It!

In your group, send:
```
I transferred $100 to @alice
```

Bot should respond:
```
✅ Transfer recorded!
💸 $100.00 from @you to @alice

Updated balances:
• @you: $900.00
• @alice: $1100.00
```

## 📝 Commands

```
/mybalance  - Check your balance
/balances   - See all balances
/history    - View transactions
/help       - Show help
```

## 🎯 How to Use

Just announce transfers naturally:
- "I transferred $100 to @alice"
- "Sent $50 to @bob"
- "@charlie I sent you $75"

Bot auto-detects and updates balances!

## 🐛 Issues?

**Bot not responding?**
- Check bot is admin in group
- Check logs: `tail -f logs/bot.log`

**Transfers not detected?**
- Use clear format: "I transferred $X to @user"
- Use @mentions
- Use past tense

**Dependencies failed?**
- See [DEPENDENCY_FIX.md](DEPENDENCY_FIX.md)
- Or use minimal: `pip install -r requirements-minimal.txt`

## 📚 More Info

- **GROUP_BOT_GUIDE.md** - Complete guide
- **FINAL_GROUP_BOT_SUMMARY.md** - Full summary
- **AI_FEATURES.md** - AI details

## 🎉 That's It!

Your bot is ready! Add to group and start tracking transfers!

---

**Questions?** Check the logs or documentation!
