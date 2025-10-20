# Fix: Bot Not Reading Group Messages

## Problem

Bot only receives commands but not regular messages in the group.

## Root Cause

**Privacy Mode** is enabled. By default, Telegram bots only receive:
- Commands (starting with /)
- Messages that mention the bot
- Replies to bot's messages

To detect transfer announcements, the bot needs to read ALL messages.

## Solution: Disable Privacy Mode

### Step 1: Open BotFather

1. Open Telegram
2. Search for `@BotFather`
3. Start a chat

### Step 2: Disable Privacy Mode

Send these commands to BotFather:

```
/mybots
```

Select your bot from the list.

```
Bot Settings
```

```
Group Privacy
```

```
Turn off
```

You should see:
```
Privacy mode is disabled for YourBot. 
The bot will receive all messages in groups.
```

### Step 3: Remove and Re-add Bot to Group

**IMPORTANT:** You must remove the bot and add it again for the change to take effect!

1. Remove bot from the group
2. Wait 5 seconds
3. Add bot back to the group
4. Make bot admin again

### Step 4: Test

Send a message in the group:
```
I transferred $100 to @alice
```

Bot should now respond!

## Quick Fix Commands

```
1. Message @BotFather
2. /mybots
3. Select your bot
4. Bot Settings
5. Group Privacy
6. Turn off
7. Remove bot from group
8. Add bot back
9. Make admin
10. Test!
```

## Verify It's Working

Check the logs:
```bash
tail -f logs/bot.log
```

You should see:
```
INFO - Processing group message from username: message text...
```

If you see this, privacy mode is disabled correctly!

## Alternative: Check Current Status

To check if privacy mode is disabled:

1. Message @BotFather
2. `/mybots`
3. Select your bot
4. `Bot Settings`
5. `Group Privacy`

It should show: **"Privacy mode is disabled"**

## Still Not Working?

### Check 1: Bot Permissions

Make sure bot is admin with these permissions:
- ✅ Read Messages (most important!)
- ✅ Send Messages
- ✅ Delete Messages (optional)

### Check 2: Bot is Running

```bash
ps aux | grep python
```

Should show your bot process.

### Check 3: Logs

```bash
tail -f logs/bot.log
```

Send a message in the group and watch for:
```
INFO - Processing group message from...
```

If you don't see this, privacy mode is still enabled.

### Check 4: Restart Bot

After changing privacy mode:
```bash
# Stop bot
Ctrl+C

# Start bot
python run.py
```

## Summary

**Privacy Mode = ON** (default)
- ❌ Bot only gets commands
- ❌ Bot can't detect transfers
- ❌ Bot can't auto-register users

**Privacy Mode = OFF** (required)
- ✅ Bot gets all messages
- ✅ Bot can detect transfers
- ✅ Bot can auto-register users

## Complete Steps

1. ✅ Message @BotFather
2. ✅ `/mybots` → Select your bot
3. ✅ `Bot Settings` → `Group Privacy` → `Turn off`
4. ✅ Remove bot from group
5. ✅ Add bot back to group
6. ✅ Make bot admin
7. ✅ Test: "I transferred $100 to @alice"

---

**This is the most common issue!** Privacy mode must be disabled for the bot to work in groups.
