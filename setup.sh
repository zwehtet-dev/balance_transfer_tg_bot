#!/bin/bash
# Setup script for Balance Transfer Bot v2.0

echo "🤖 Setting up Balance Transfer Bot v2.0..."
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your TELEGRAM_BOT_TOKEN"
else
    echo "✓ .env file already exists"
fi

# Create required directories
echo "📁 Creating directories..."
mkdir -p data
mkdir -p logs
mkdir -p backups

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env and add your bot token from @BotFather"
echo "   nano .env"
echo ""
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Run the bot:"
echo "   python run.py"
echo ""
echo "4. Or use make commands:"
echo "   make run      # Run the bot"
echo "   make test     # Run tests"
echo "   make db-shell # Open database"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Main documentation"
echo "   - QUICK_REFERENCE.md - Quick reference"
echo "   - V2_SUMMARY.md - What's new in v2.0"
echo ""
