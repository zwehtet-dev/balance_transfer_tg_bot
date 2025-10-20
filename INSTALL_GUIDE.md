# Installation Guide

## Option 1: Full Installation (with AI Features)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter dependency conflicts, try:

```bash
# Install in order
pip install python-telegram-bot==20.7 python-dotenv==1.0.0
pip install langchain==0.1.20
pip install langchain-mistralai==0.1.0
pip install langchain-openai==0.1.7
```

### Step 2: Configure

```bash
cp .env.example .env
nano .env  # Add your tokens
```

### Step 3: Run

```bash
python run.py
```

---

## Option 2: Minimal Installation (without AI)

If you don't need AI features or have dependency issues:

### Step 1: Install Minimal Dependencies

```bash
pip install -r requirements-minimal.txt
```

### Step 2: Disable AI in Configuration

Edit `.env`:
```bash
ENABLE_AI=false
```

### Step 3: Run

```bash
python run.py
```

The bot will work with traditional commands only (/transfer, /balance, etc.)

---

## Troubleshooting

### Dependency Conflicts

If you get `ResolutionImpossible` error:

**Solution 1: Use Virtual Environment**
```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install
pip install --upgrade pip
pip install -r requirements.txt
```

**Solution 2: Install Without AI**
```bash
pip install -r requirements-minimal.txt
# Set ENABLE_AI=false in .env
```

**Solution 3: Manual Installation**
```bash
# Install one by one
pip install python-telegram-bot==20.7
pip install python-dotenv==1.0.0
pip install langchain==0.1.20
pip install langchain-mistralai==0.1.0
```

### ImportError: No module named 'langchain'

```bash
# Make sure you're in the right environment
which python
pip list | grep langchain

# Reinstall
pip install langchain==0.1.20
```

### Mistral AI Connection Error

```bash
# Test connection
python -c "from langchain_mistralai import ChatMistralAI; print('OK')"

# Check API key
echo $MISTRAL_API_KEY
```

---

## Platform-Specific Instructions

### macOS

```bash
# Install Python 3.8+
brew install python3

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install
pip install -r requirements.txt
```

### Linux (Ubuntu/Debian)

```bash
# Install Python 3.8+
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install
pip install -r requirements.txt
```

### Windows

```bash
# Install Python 3.8+ from python.org

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install
pip install -r requirements.txt
```

---

## Verification

After installation, verify everything works:

```bash
# Check Python version
python --version  # Should be 3.8+

# Check installed packages
pip list | grep telegram
pip list | grep langchain

# Test imports
python -c "from telegram.ext import Application; print('Telegram: OK')"
python -c "from langchain_mistralai import ChatMistralAI; print('LangChain: OK')"

# Run bot
python run.py
```

---

## Docker Installation (Alternative)

If you prefer Docker:

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# View logs
docker-compose logs -f
```

---

## Common Issues

### Issue: "No module named 'telegram'"
**Solution:** `pip install python-telegram-bot==20.7`

### Issue: "No module named 'langchain'"
**Solution:** `pip install langchain==0.1.20`

### Issue: "No module named 'langchain_mistralai'"
**Solution:** `pip install langchain-mistralai==0.1.0`

### Issue: Dependency conflicts
**Solution:** Use virtual environment or install minimal version

### Issue: Bot doesn't start
**Solution:** Check `.env` file has TELEGRAM_BOT_TOKEN

---

## Getting Help

1. Check logs: `tail -f logs/bot.log`
2. Verify configuration: `cat .env`
3. Test dependencies: `pip list`
4. Try minimal installation: `pip install -r requirements-minimal.txt`

---

## Next Steps

After successful installation:

1. **Configure**: Edit `.env` with your tokens
2. **Test**: Run `python run.py`
3. **Use**: Send `/start` to your bot in Telegram
4. **AI Setup**: See [SETUP_AI.md](SETUP_AI.md) for AI features

---

**Need help?** Check the documentation or logs!
