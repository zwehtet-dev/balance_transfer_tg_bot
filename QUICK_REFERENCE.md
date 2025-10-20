# Quick Reference Card - Bot v2.0

## 🚀 Quick Start

```bash
# 1. Setup
cp .env.example .env
nano .env  # Add your TELEGRAM_BOT_TOKEN

# 2. Run
python run.py
```

## 📁 Project Structure

```
bot/
├── main.py              # Entry point
├── models/              # Database & models
├── services/            # Business logic
├── handlers/            # Telegram commands
└── utils/               # Config & logging
```

## 🗄️ Database

```bash
# View database
sqlite3 data/bot.db

# Useful queries
SELECT * FROM users;
SELECT * FROM transactions ORDER BY created_at DESC LIMIT 10;
SELECT COUNT(*) FROM transactions;

# Exit
.quit
```

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| `/balance` | Check balances |
| `/transfer` | Transfer money |
| `/history` | View transactions |
| `/stats` | View statistics |
| `/reset` | Reset balances |
| `/help` | Show help |

## 💻 Code Examples

### Get User Balance
```python
from bot.services.user_service import UserService

user_service = UserService(db)
user = user_service.get_by_name("person_a")
print(f"Balance: ${user.balance:.2f}")
```

### Make Transfer
```python
from bot.services.balance_service import BalanceService

balance_service = BalanceService(db)
result = balance_service.transfer("person_a", "person_b", 100.0)

if result.success:
    print(result.message)
else:
    print(f"Failed: {result.message}")
```

### Get Transaction History
```python
from bot.services.transaction_service import TransactionService

transaction_service = TransactionService(db)
transactions = transaction_service.get_recent(limit=10)

for tx in transactions:
    print(tx.format_display())
```

### Create New User
```python
user_service = UserService(db)
new_user = user_service.create("person_c", 1000.0)
print(f"Created: {new_user.name}")
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_balance_service.py::TestBalanceService::test_transfer_success -v

# With coverage
pytest tests/ --cov=bot --cov-report=html

# View coverage
open htmlcov/index.html
```

## 📝 Configuration

### Environment Variables
```bash
TELEGRAM_BOT_TOKEN=your_token_here
DATABASE_URL=data/bot.db
DEFAULT_BALANCE=1000.0
MAX_TRANSACTION_HISTORY=10
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
```

### Config in Code
```python
from bot.utils.config import BotConfig

config = BotConfig.from_env()
print(config.database_url)
print(config.default_balance)
```

## 🔧 Common Tasks

### Add New Command
```python
# 1. In bot/handlers/command_handlers.py
async def my_command(self, update, context):
    await update.message.reply_text("Hello!")

# 2. In bot/services/bot_service.py
self.application.add_handler(
    CommandHandler("mycommand", self.handlers.my_command)
)
```

### Add New Service Method
```python
# In bot/services/balance_service.py
def get_user_stats(self, user_name: str) -> dict:
    user = self.user_service.get_by_name(user_name)
    transactions = self.transaction_service.get_by_user(user.id)
    return {
        'balance': user.balance,
        'transaction_count': len(transactions)
    }
```

### Backup Database
```bash
# Manual backup
cp data/bot.db data/bot.db.backup

# Automated backup script
sqlite3 data/bot.db ".backup data/bot_$(date +%Y%m%d_%H%M%S).db"
```

### Reset Database
```bash
# Delete database
rm data/bot.db

# Restart bot (will recreate)
python run.py
```

## 🐛 Debugging

### Check Logs
```bash
# View logs
tail -f logs/bot.log

# Search for errors
grep ERROR logs/bot.log

# Last 50 lines
tail -n 50 logs/bot.log
```

### Enable Debug Mode
```bash
# In .env
LOG_LEVEL=DEBUG

# Or temporarily
export LOG_LEVEL=DEBUG
python run.py
```

### Database Issues
```bash
# Check database integrity
sqlite3 data/bot.db "PRAGMA integrity_check;"

# Check table structure
sqlite3 data/bot.db ".schema users"
sqlite3 data/bot.db ".schema transactions"

# Check indexes
sqlite3 data/bot.db ".indexes"
```

## 📊 Monitoring

### Check Bot Status
```bash
# Check if running
ps aux | grep "python.*run.py"

# Check memory usage
ps aux | grep python | awk '{print $4, $11}'

# Check database size
ls -lh data/bot.db
```

### View Statistics
```python
from bot.services.balance_service import BalanceService

balance_service = BalanceService(db)
users = balance_service.user_service.get_all()
tx_count = balance_service.transaction_service.get_count()

print(f"Users: {len(users)}")
print(f"Transactions: {tx_count}")
```

## 🔄 Maintenance

### Daily Tasks
```bash
# Check logs for errors
grep ERROR logs/bot.log

# Backup database
cp data/bot.db backups/bot_$(date +%Y%m%d).db

# Check disk space
df -h
```

### Weekly Tasks
```bash
# Rotate logs
mv logs/bot.log logs/bot_$(date +%Y%m%d).log
touch logs/bot.log

# Clean old backups (keep last 7 days)
find backups/ -name "bot_*.db" -mtime +7 -delete

# Update dependencies
pip list --outdated
```

## 🚨 Troubleshooting

### Bot Not Responding
```bash
# 1. Check if running
ps aux | grep python

# 2. Check logs
tail -f logs/bot.log

# 3. Restart bot
pkill -f run.py
python run.py
```

### Database Locked
```bash
# 1. Stop all bot instances
pkill -f run.py

# 2. Remove journal file
rm data/bot.db-journal

# 3. Restart
python run.py
```

### Import Errors
```bash
# 1. Check Python path
python -c "import sys; print(sys.path)"

# 2. Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# 3. Check imports
python -c "from bot.models import User; print('OK')"
```

## 📚 Resources

### Documentation
- `README_V2.md` - Complete guide
- `MIGRATION_GUIDE.md` - v1 → v2 migration
- `PROJECT_STRUCTURE_V2.txt` - Structure overview
- `V2_SUMMARY.md` - What's new

### Code Navigation
- Entry point: `bot/main.py`
- Business logic: `bot/services/balance_service.py`
- Database: `bot/models/database.py`
- Commands: `bot/handlers/command_handlers.py`

### External Links
- [python-telegram-bot docs](https://docs.python-telegram-bot.org/)
- [SQLite docs](https://www.sqlite.org/docs.html)
- [pytest docs](https://docs.pytest.org/)

## 🎯 Cheat Sheet

```bash
# Development
python run.py                    # Run bot
pytest tests/ -v                 # Run tests
sqlite3 data/bot.db             # Open database

# Debugging
tail -f logs/bot.log            # Watch logs
export LOG_LEVEL=DEBUG          # Debug mode
python -m pdb run.py            # Debug with pdb

# Maintenance
cp data/bot.db backup.db        # Backup
rm data/bot.db                  # Reset
pip install -r requirements.txt # Update deps

# Database
sqlite3 data/bot.db "SELECT * FROM users;"
sqlite3 data/bot.db "SELECT COUNT(*) FROM transactions;"
sqlite3 data/bot.db ".schema"
```

---

**Quick Help:** For detailed information, see `README_V2.md`  
**Version:** 2.0.0  
**Last Updated:** 2024-10-20
