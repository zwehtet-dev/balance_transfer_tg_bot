# Telegram Balance Transfer Bot v2.0

A professional, scalable Telegram bot for managing balance transfers with SQLite database storage.

## 🚀 Features

- 💰 Real-time balance tracking
- 💸 Secure money transfers between users
- 📊 Unlimited transaction history (SQLite)
- 🔄 Balance reset functionality
- 💾 Persistent database storage
- ✅ Input validation and error handling
- 🔒 Insufficient funds protection
- 📈 Statistics and analytics
- 🏗️ Scalable architecture

## 📁 Project Structure

```
bot/
├── main.py                    # Application entry point
├── models/                    # Data models & database
│   ├── __init__.py
│   ├── database.py           # Database connection & schema
│   ├── user.py               # User model
│   └── transaction.py        # Transaction model
├── services/                  # Business logic layer
│   ├── __init__.py
│   ├── balance_service.py    # Balance & transfer logic
│   ├── user_service.py       # User operations
│   ├── transaction_service.py # Transaction operations
│   └── bot_service.py        # Main bot orchestration
├── handlers/                  # Telegram command handlers
│   ├── __init__.py
│   └── command_handlers.py   # All bot commands
└── utils/                     # Utilities
    ├── __init__.py
    ├── config.py             # Configuration management
    └── logger.py             # Logging setup
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo>
cd telegram_bot

# Run automated setup
./setup.sh
```

Or manually:

```bash
# Install dependencies
pip install -r requirements.txt

# Create configuration
cp .env.example .env
nano .env  # Add your TELEGRAM_BOT_TOKEN
```

### 2. Configuration

Edit `.env` with your bot token from [@BotFather](https://t.me/BotFather):

```bash
TELEGRAM_BOT_TOKEN=your_token_from_botfather
DATABASE_URL=data/bot.db
DEFAULT_BALANCE=1000.0
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
```

### 3. Run the Bot

```bash
# Using run script
python run.py

# Or using make
make run

# Or directly
python -m bot.main
```

## 📝 Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and command list |
| `/balance` | Check current balances |
| `/transfer` | Transfer money between users |
| `/history` | View recent transactions |
| `/stats` | View bot statistics (NEW!) |
| `/reset` | Reset all balances to default |
| `/help` | Show detailed help |

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    balance REAL NOT NULL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_user_id INTEGER NOT NULL,
    to_user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    balance_from REAL NOT NULL,
    balance_to REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (from_user_id) REFERENCES users(id),
    FOREIGN KEY (to_user_id) REFERENCES users(id)
);
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=bot --cov-report=html

# Run specific test file
pytest tests/test_balance_service.py -v

# Using make
make test
```

## 💻 Development

### Adding a New Command

```python
# In bot/handlers/command_handlers.py
async def my_command(self, update, context):
    await update.message.reply_text("Hello!")

# In bot/services/bot_service.py
self.application.add_handler(
    CommandHandler("mycommand", self.handlers.my_command)
)
```

### Creating a New User

```python
from bot.services.user_service import UserService

user_service = UserService(db)
new_user = user_service.create("person_c", 1000.0)
```

### Making a Transfer

```python
from bot.services.balance_service import BalanceService

balance_service = BalanceService(db)
result = balance_service.transfer("person_a", "person_b", 100.0)

if result.success:
    print(result.message)
```

## ⚙️ Configuration

Environment variables (see `.env.example`):

- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token (required)
- `DATABASE_URL` - Path to SQLite database (default: `data/bot.db`)
- `DEFAULT_BALANCE` - Initial balance for users (default: `1000.0`)
- `MAX_TRANSACTION_HISTORY` - History display limit (default: `10`)
- `LOG_LEVEL` - Logging level (default: `INFO`)
- `LOG_FILE` - Log file path (default: `logs/bot.log`)

## 🏗️ Architecture

### Layered Architecture

```
┌─────────────────────────────────────┐
│     Telegram Bot API (External)     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Handlers (command_handlers.py)    │  ← Presentation Layer
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Services (balance_service.py)     │  ← Business Logic
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Models (user.py, transaction.py)  │  ← Domain Models
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Database (SQLite)                 │  ← Data Storage
└─────────────────────────────────────┘
```

### Design Patterns

- **Service Layer Pattern**: Business logic separated from presentation
- **Repository Pattern**: Data access abstraction (UserService, TransactionService)
- **Dependency Injection**: Components receive dependencies through constructors
- **Result Object Pattern**: Rich return values for operations
- **Factory Pattern**: Database initialization and model creation

## 🔒 Security Features

- ✅ Environment-based configuration (no hardcoded secrets)
- ✅ SQL injection protection (parameterized queries)
- ✅ Input validation at multiple layers
- ✅ Balance cannot go negative
- ✅ Atomic database transactions
- ✅ Comprehensive error handling
- ✅ Secure logging (no sensitive data)

## 📊 Performance

- ✅ Database indexes for fast queries
- ✅ Connection pooling
- ✅ Efficient SQL queries
- ✅ Async/await for non-blocking operations
- ✅ Minimal memory footprint

## 🐛 Troubleshooting

### Database locked error
```bash
# Check if another instance is running
ps aux | grep python

# Remove lock if needed
rm data/bot.db-journal
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check imports
python -c "from bot.models import User; print('OK')"
```

### View database
```bash
# Open SQLite shell
make db-shell

# Or directly
sqlite3 data/bot.db
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 📚 Documentation

- **README.md** - This file (main documentation)
- **QUICK_REFERENCE.md** - Quick reference card
- **MIGRATION_GUIDE.md** - Migration guide from older versions
- **PROJECT_STRUCTURE_V2.txt** - Detailed structure overview
- **V2_SUMMARY.md** - Version 2.0 summary
- **CHANGELOG.md** - Version history

## 🚦 What's New in v2.0

- ✅ **SQLite Database** - Replaced JSON with proper database
- ✅ **Scalable Architecture** - Modular design with clear separation
- ✅ **Service Layer** - Clean business logic separation
- ✅ **Unlimited History** - All transactions stored in database
- ✅ **Better Performance** - Indexed queries for fast lookups
- ✅ **New /stats Command** - View bot statistics
- ✅ **Enhanced Testing** - Comprehensive test suite
- ✅ **Production Ready** - Robust error handling and logging

## 🛠️ Make Commands

```bash
make help      # Show available commands
make install   # Install dependencies
make run       # Run the bot
make test      # Run tests
make db-shell  # Open database shell
make backup    # Backup database
make clean     # Clean up generated files
```

## 📄 License

MIT License

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📞 Support

- Documentation: See files in this repository
- Issues: GitHub Issues
- Quick Reference: See QUICK_REFERENCE.md

---

**Version:** 2.0.0  
**Database:** SQLite  
**Python:** 3.8+  
**Framework:** python-telegram-bot 20.7  
**Architecture:** Layered, Service-Oriented
