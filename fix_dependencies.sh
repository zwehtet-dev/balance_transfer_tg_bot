#!/bin/bash
# Fix dependency installation issues

echo "🔧 Fixing dependency installation..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies in order
echo "📥 Installing dependencies..."
echo ""

echo "1/5 Installing core dependencies..."
pip install python-telegram-bot==20.7 python-dotenv==1.0.0

echo "2/5 Installing LangChain core..."
pip install langchain==0.1.20

echo "3/5 Installing Mistral AI..."
pip install langchain-mistralai==0.1.0

echo "4/5 Installing OpenAI (optional)..."
pip install langchain-openai==0.1.7 || echo "⚠️  OpenAI installation failed (optional)"

echo "5/5 Installing dev dependencies (optional)..."
pip install pytest pytest-asyncio pytest-cov pytest-mock || echo "⚠️  Dev dependencies failed (optional)"

echo ""
echo "✅ Installation complete!"
echo ""
echo "📋 Verify installation:"
python -c "from telegram.ext import Application; print('✅ Telegram: OK')" || echo "❌ Telegram: FAILED"
python -c "from langchain_mistralai import ChatMistralAI; print('✅ LangChain: OK')" || echo "❌ LangChain: FAILED (AI features disabled)"
echo ""
echo "🚀 Next steps:"
echo "1. Edit .env with your tokens"
echo "2. Run: python run.py"
echo ""
