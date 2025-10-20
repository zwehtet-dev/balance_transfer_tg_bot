# Dependency Installation Fix

## Problem

Getting `ResolutionImpossible` error when installing dependencies.

## Quick Fix

### Option 1: Use Fix Script (Recommended)

```bash
chmod +x fix_dependencies.sh
./fix_dependencies.sh
```

This will install dependencies in the correct order.

### Option 2: Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install in order
pip install python-telegram-bot==20.7 python-dotenv==1.0.0
pip install langchain==0.1.20
pip install langchain-mistralai==0.1.0
pip install langchain-openai==0.1.7
```

### Option 3: Install Without AI

If you don't need AI features:

```bash
pip install -r requirements-minimal.txt
```

Then set in `.env`:
```bash
ENABLE_AI=false
```

## Verification

After installation, verify:

```bash
# Check Telegram
python -c "from telegram.ext import Application; print('OK')"

# Check LangChain (if AI enabled)
python -c "from langchain_mistralai import ChatMistralAI; print('OK')"

# Run bot
python run.py
```

## Why This Happens

LangChain has many dependencies that can conflict. Installing in order helps pip resolve them correctly.

## Alternative: Use Docker

If you continue having issues:

```bash
docker-compose up -d
```

This uses a clean environment with all dependencies pre-installed.

## Still Having Issues?

1. **Use Python 3.8-3.11**: LangChain works best with these versions
   ```bash
   python --version
   ```

2. **Clear pip cache**:
   ```bash
   pip cache purge
   ```

3. **Use minimal installation**:
   ```bash
   pip install -r requirements-minimal.txt
   # Set ENABLE_AI=false in .env
   ```

4. **Check logs**:
   ```bash
   tail -f logs/bot.log
   ```

## Success!

Once installed, you should see:
```
✅ Telegram: OK
✅ LangChain: OK
```

Then you can run:
```bash
python run.py
```

---

**Need more help?** See [INSTALL_GUIDE.md](INSTALL_GUIDE.md)
