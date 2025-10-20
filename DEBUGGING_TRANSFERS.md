# Debugging Transfer Detection

## Common Issues & Solutions

### Issue 1: "User not found"

**Problem:** Bot detects transfer but can't find the receiver.

**Why:** User hasn't sent a message in the group yet, so they're not registered.

**Solution:**
1. Ask the receiver to send ANY message in the group
2. Bot will auto-register them with $1000
3. Try the transfer again

**Check registered users:**
```
/users
```

### Issue 2: Transfer not detected

**Problem:** Bot doesn't respond to transfer message.

**Checklist:**
- ✅ Bot is admin in the group
- ✅ Message format is clear
- ✅ Using past tense ("I transferred" not "I will transfer")
- ✅ Amount is specified ($100 or 100)
- ✅ Receiver is mentioned

**Good formats:**
```
✅ I transferred $100 to @alice
✅ I sent $50 to @bob
✅ Sent $75 to @charlie
✅ @dave I sent you $200
```

**Bad formats:**
```
❌ maybe send 100 to alice
❌ I will transfer $100
❌ please send me $100
❌ thinking about sending
```

### Issue 3: Username with special characters

**Problem:** Username like "Chue Chue🦋" not found.

**Solution:** Bot now matches by:
1. Exact username
2. First name (partial match)
3. Last name (partial match)

**Example:**
- User: "Chue Chue🦋"
- Can mention as: "Chue", "@Chue", "Chue Chue"

### Issue 4: Check what bot detected

**View logs:**
```bash
tail -f logs/bot.log | grep "Transfer detection"
```

You'll see:
```
Transfer detection: is_transfer=True, confidence=0.90, from=alice, to=bob, amount=100.0
```

**Confidence levels:**
- 0.9-1.0: High confidence (will process)
- 0.7-0.9: Medium confidence (will process)
- < 0.7: Low confidence (ignored)

## Testing Steps

### Step 1: Register Users

```
Alice: Hi everyone!
Bot: (registers Alice with $1000)

Bob: Hello!
Bot: (registers Bob with $1000)
```

### Step 2: Check Users

```
/users
```

Response:
```
👥 Registered Users:

1. @alice
2. @bob

💡 Total: 2 users
```

### Step 3: Test Transfer

```
Alice: I transferred $100 to @bob
```

Bot should respond:
```
✅ Transfer recorded!
💸 $100.00 from @alice to @bob

Updated balances:
• @alice: $900.00
• @bob: $1100.00
```

### Step 4: Verify Balances

```
/balances
```

Response:
```
💰 Group Balances

1. @bob: $1100.00
2. @alice: $900.00

📊 Total: $2000.00
👥 Members: 2
```

## Commands for Debugging

```
/users      - See who's registered
/mybalance  - Check your balance
/balances   - See all balances
/history    - View recent transfers
/help       - Show help
```

## Logs to Check

**Transfer detected:**
```
INFO - Transfer detected! From: alice, To: bob, Amount: 100.0
```

**User not found:**
```
WARNING - User 'bob' not found. Available users: @alice, @charlie
```

**Transfer completed:**
```
INFO - Transfer completed: @alice -> @bob, $100.00
```

## Quick Fixes

### Fix 1: User Not Registered

```
# Ask user to send any message
User: hi

# Bot auto-registers them
# Try transfer again
```

### Fix 2: Unclear Message

```
# Bad
I sent money to bob

# Good
I transferred $100 to @bob
```

### Fix 3: Check Bot Permissions

```
1. Go to group settings
2. Administrators
3. Check bot has "Read Messages" permission
```

## Testing Checklist

- [ ] Bot is admin in group
- [ ] Bot is running (`python run.py`)
- [ ] Users have sent at least one message
- [ ] Transfer message is clear
- [ ] Amount is specified
- [ ] Receiver is mentioned
- [ ] Using past tense

## Still Not Working?

1. **Check logs:**
   ```bash
   tail -f logs/bot.log
   ```

2. **Test with simple message:**
   ```
   I transferred $10 to @username
   ```

3. **Verify users:**
   ```
   /users
   ```

4. **Check AI is working:**
   ```bash
   grep "AI service initialized" logs/bot.log
   ```

5. **Restart bot:**
   ```bash
   # Stop: Ctrl+C
   # Start: python run.py
   ```

## Example Session

```
# 1. Users join
Alice: Hello!
Bob: Hi there!

# 2. Check users
/users
→ Shows: @alice, @bob

# 3. Transfer
Alice: I transferred $100 to @bob
→ Bot confirms transfer

# 4. Check balances
/balances
→ Shows updated balances

# 5. View history
/history
→ Shows transaction
```

## Success!

When working correctly, you'll see:
1. ✅ Bot detects transfer message
2. ✅ Finds both users
3. ✅ Updates balances
4. ✅ Sends confirmation
5. ✅ Records in history

---

**Still having issues?** Check the logs and make sure users are registered!
