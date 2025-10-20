# Complete Setup Checklist

## ✅ Step-by-Step Setup

### 1. Get Bot Token
- [ ] Message @BotFather on Telegram
- [ ] Send `/newbot`
- [ ] Follow prompts
- [ ] Copy token

### 2. **CRITICAL: Disable Privacy Mode**
- [ ] Message @BotFather
- [ ] Send `/mybots`
- [ ] Select your bot
- [ ] Click "Bot Settings"
- [ ] Click "Group Privacy"
- [ ] Click "Turn off"
- [ ] Confirm: "Privacy mode is disabled"

**⚠️ THIS IS THE MOST IMPORTANT STEP!**

### 3. Get Mistral AI Key
- [ ] Visit https://console.mistral.ai/
- [ ] Sign up (free)
- [ ] Create API key
- [ ] Copy key

### 4. Configure Bot
- [ ] Edit `.env` file
- [ ] Add `TELEGRAM_BOT_TOKEN=your_token`
- [ ] Add `MISTRAL_API_KEY=your_key`
- [ ] Set `ENABLE_AI=true`

### 5. Install Dependencies
- [ ] Run `./fix_dependencies.sh`
- [ ] Or `pip install -r requirements.txt`

### 6. Start Bot
- [ ] Run `python run.py`
- [ ] Check logs show "Bot is running"

### 7. Add Bot to Group
- [ ] Add bot to your Telegram group
- [ ] Go to group settings → Administrators
- [ ] Add bot as admin
- [ ] Enable "Read Messages" permission

### 8. Test Bot
- [ ] Send `/help` in group
- [ ] Bot should respond
- [ ] Send "hi" in group
- [ ] Check logs: should see "Processing group message"

### 9. Register Users
- [ ] Each user sends any message
- [ ] Bot auto-registers them
- [ ] Check with `/users`

### 10. Test Transfer
- [ ] Send: "I transferred $100 to @username"
- [ ] Bot should detect and respond
- [ ] Check with `/balances`

## 🚨 Common Issues

### Issue: Bot only responds to commands

**Cause:** Privacy mode is enabled

**Fix:**
1. Message @BotFather
2. `/mybots` → Select bot
3. Bot Settings → Group Privacy → Turn OFF
4. **Remove bot from group**
5. **Add bot back to group**
6. Make admin again

### Issue: "User not found"

**Cause:** User hasn't sent a message yet

**Fix:**
1. Ask user to send any message
2. Bot will auto-register them
3. Try transfer again

### Issue: Transfer not detected

**Cause:** Message format unclear

**Fix:** Use clear format:
```
I transferred $100 to @username
```

## ✅ Verification

### Check 1: Privacy Mode
```
@BotFather → /mybots → Your Bot → Bot Settings → Group Privacy
Should show: "Privacy mode is disabled"
```

### Check 2: Bot Receives Messages
```bash
tail -f logs/bot.log
```
Send "test" in group. Should see:
```
INFO - Processing group message from username: test...
```

### Check 3: Users Registered
```
/users
```
Should list all users who sent messages.

### Check 4: Transfer Works
```
User: I transferred $100 to @alice
Bot: ✅ Transfer recorded! ...
```

## 📋 Quick Test

```
1. /help          → Bot responds
2. hi             → Check logs (should see "Processing group message")
3. /users         → Shows registered users
4. I transferred $10 to @user → Bot detects and processes
5. /balances      → Shows updated balances
```

## 🎯 Success Criteria

- ✅ Privacy mode is OFF
- ✅ Bot is admin in group
- ✅ Bot receives all messages (check logs)
- ✅ Users can register by sending messages
- ✅ Transfers are detected and processed
- ✅ Balances update correctly

## 📞 Still Not Working?

1. **Check privacy mode** (most common issue!)
2. **Check logs:** `tail -f logs/bot.log`
3. **Restart bot:** Stop and start again
4. **Remove and re-add bot** to group
5. **Read:** `FIX_BOT_PRIVACY.md`

---

**Most Important:** Privacy mode MUST be disabled!
