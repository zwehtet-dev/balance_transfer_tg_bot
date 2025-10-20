# Quick Setup Guide - AI Features

## Step 1: Get Mistral AI API Key (Free)

1. Visit https://console.mistral.ai/
2. Sign up for a free account
3. Go to "API Keys" section
4. Click "Create new key"
5. Copy the API key

## Step 2: Update Configuration

Edit your `.env` file:

```bash
# AI Configuration
AI_PROVIDER=mistral
MISTRAL_API_KEY=your_actual_mistral_key_here
AI_MODEL=mistral-small-latest
ENABLE_AI=true

# Group Monitoring (optional)
MONITOR_GROUPS=true
AUTO_DETECT_TRANSFERS=true
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Run the Bot

```bash
python run.py
```

## Step 5: Test Natural Language

Open Telegram and message your bot:

```
send 100 to @alice
```

The bot should understand and execute the transfer!

## Step 6: Test Group Detection (Optional)

1. Add bot to a Telegram group
2. Get the group ID from logs
3. Update `.env`:
   ```bash
   TELEGRAM_GROUP_ID=-1001234567890
   ```
4. In the group, send:
   ```
   @alice I sent you $50
   ```

The bot should auto-detect and record the transfer!

## Troubleshooting

### "MISTRAL_API_KEY not found"
- Make sure you added the key to `.env`
- Restart the bot after updating `.env`

### "AI service not available"
- Check your API key is valid
- Check internet connection
- Check Mistral AI status: https://status.mistral.ai/

### Bot doesn't respond to natural language
- Make sure `ENABLE_AI=true` in `.env`
- Check logs: `tail -f logs/bot.log`
- Try a clear command: "send 100 to alice"

## What's Next?

- Read [AI_FEATURES.md](AI_FEATURES.md) for detailed documentation
- Customize prompts in `bot/services/ai_service.py`
- Add more users to the mapping
- Set up group monitoring

## Cost

Mistral AI free tier includes:
- Limited requests per month
- Perfect for testing and small deployments

For production, consider:
- Mistral AI paid tier
- Or switch to OpenAI (set `AI_PROVIDER=openai`)

---

**Need Help?** Check the logs or open an issue!
