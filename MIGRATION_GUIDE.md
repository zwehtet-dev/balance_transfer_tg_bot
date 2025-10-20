# Migration Guide: v1.0 to v2.0

This guide helps you migrate from the JSON-based v1.0 to the SQLite-based v2.0.

## Overview of Changes

### Architecture Changes

| Aspect | v1.0 | v2.0 |
|--------|------|------|
| **Storage** | JSON file | SQLite database |
| **Structure** | `balance_bot/` | `bot/` |
| **Models** | Single file | Separate files per model |
| **Services** | Combined | Separated (User, Transaction, Balance) |
| **Database** | File I/O | SQL queries with indexes |

### Directory Structure

**v1.0:**
```
balance_bot/
├── main.py
├── bot.py
├── config.py
├── handlers.py
├── services.py
├── models.py
└── storage.py
```

**v2.0:**
```
bot/
├── main.py
├── models/
│   ├── database.py
│   ├── user.py
│   └── transaction.py
├── services/
│   ├── balance_service.py
│   ├── user_service.py
│   ├── transaction_service.py
│   └── bot_service.py
├── handlers/
│   └── command_handlers.py
└── utils/
    ├── config.py
    └── logger.py
```

## Migration Steps

### Step 1: Backup Your Data

```bash
# Backup JSON data
cp data/balances.json data/balances.json.backup

# Backup logs
cp bot.log bot.log.backup
```

### Step 2: Install New Dependencies

```bash
# Update requirements
pip install -r requirements.txt
```

### Step 3: Update Configuration

**Old .env:**
```bash
TELEGRAM_BOT_TOKEN=your_token
STORAGE_PATH=data/balances.json
```

**New .env:**
```bash
TELEGRAM_BOT_TOKEN=your_token
DATABASE_URL=data/bot.db
LOG_FILE=logs/bot.log
```

### Step 4: Migrate Data (Optional)

If you want to preserve transaction history, use this migration script:

```python
# migrate_data.py
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from bot.models.database import Database, init_database
from bot.services.user_service import UserService

def migrate():
    # Load old JSON data
    try:
        with open('data/balances.json', 'r') as f:
            old_data = json.load(f)
    except FileNotFoundError:
        print("No old data found, starting fresh")
        return
    
    # Initialize new database
    db = Database('data/bot.db')
    init_database(db)
    user_service = UserService(db)
    
    # Migrate user balances
    if 'users' in old_data:
        for name, balance in old_data['users'].items():
            user = user_service.get_by_name(name)
            if user:
                user_service.update_balance(user.id, balance)
                print(f"Migrated {name}: ${balance:.2f}")
    
    print("Migration complete!")
    db.close()

if __name__ == '__main__':
    migrate()
```

Run migration:
```bash
python migrate_data.py
```

### Step 5: Update Import Statements

If you have custom code importing from the bot:

**Old imports:**
```python
from balance_bot.models import User, Transaction
from balance_bot.services import BalanceService
from balance_bot.config import BotConfig
```

**New imports:**
```python
from bot.models import User, Transaction
from bot.services import BalanceService
from bot.utils.config import BotConfig
```

### Step 6: Run the New Version

```bash
# Test run
python run.py
```

## API Changes

### User Model

**v1.0:**
```python
user = User("person_a", 1000.0)
user.debit(100.0)
user.credit(50.0)
```

**v2.0:**
```python
# Users are managed through UserService
user_service = UserService(db)
user = user_service.get_by_name("person_a")
user_service.update_balance(user.id, new_balance)
```

### Balance Service

**v1.0:**
```python
balance_manager = BalanceManager(storage)
success, message = balance_manager.transfer("person_a", "person_b", 100.0)
```

**v2.0:**
```python
balance_service = BalanceService(db)
result = balance_service.transfer("person_a", "person_b", 100.0)
if result.success:
    print(result.message)
```

### Storage

**v1.0:**
```python
storage = JSONStorage("data/balances.json")
data = storage.load()
storage.save(data)
```

**v2.0:**
```python
db = Database("data/bot.db")
init_database(db)
# Use services for all operations
```

## New Features in v2.0

### 1. Statistics Command
```python
# New /stats command shows:
# - Total users
# - Total transactions
# - Database info
```

### 2. Better Transaction History
```python
# Get transactions by user
transaction_service.get_by_user(user_id, limit=10)

# Get transaction count
transaction_service.get_count()
```

### 3. Enhanced Logging
```python
# Logs now go to both console and file
# Configurable log levels
# Better structured logging
```

### 4. Database Indexes
```sql
-- Faster queries with indexes
CREATE INDEX idx_transactions_from_user ON transactions(from_user_id);
CREATE INDEX idx_transactions_to_user ON transactions(to_user_id);
CREATE INDEX idx_transactions_created_at ON transactions(created_at DESC);
```

## Breaking Changes

### 1. Storage Interface

**Removed:**
- `StorageStrategy` abstract class
- `JSONStorage` class
- `load()` and `save()` methods

**Replaced with:**
- `Database` class
- SQL-based operations
- Service layer methods

### 2. Transaction Storage

**v1.0:** Transactions stored in memory (limited to 10)
**v2.0:** All transactions stored in database (unlimited)

### 3. User Management

**v1.0:** Users stored in dictionary
**v2.0:** Users stored in database with IDs

## Rollback Plan

If you need to rollback to v1.0:

```bash
# 1. Stop the bot
# 2. Restore old code
git checkout v1.0

# 3. Restore data
cp data/balances.json.backup data/balances.json

# 4. Restore environment
cp .env.v1.backup .env

# 5. Reinstall dependencies
pip install -r requirements.txt

# 6. Run old version
python run.py
```

## Testing After Migration

### 1. Check Balances
```bash
# In Telegram, send:
/balance
```

### 2. Test Transfer
```bash
/transfer
# Select direction
# Enter amount
# Verify balances updated
```

### 3. Check History
```bash
/history
# Should show recent transactions
```

### 4. View Stats
```bash
/stats
# New command in v2.0
```

### 5. Check Database
```bash
# Install sqlite3
sqlite3 data/bot.db

# Check users
SELECT * FROM users;

# Check transactions
SELECT * FROM transactions;

# Exit
.quit
```

## Common Issues

### Issue: "Database is locked"
**Solution:** Only one bot instance can run at a time
```bash
# Check for running instances
ps aux | grep python
# Kill old instances
kill <pid>
```

### Issue: "No such table: users"
**Solution:** Database not initialized
```bash
# Delete and recreate
rm data/bot.db
python run.py
```

### Issue: "Import errors"
**Solution:** Update import paths
```python
# Change from balance_bot to bot
from bot.models import User
```

### Issue: "Missing balances after migration"
**Solution:** Run migration script again
```bash
python migrate_data.py
```

## Performance Comparison

| Operation | v1.0 (JSON) | v2.0 (SQLite) |
|-----------|-------------|---------------|
| Read balance | O(1) | O(1) with index |
| Transfer | O(1) | O(1) |
| Get history | O(n) | O(log n) with index |
| Search transactions | O(n) | O(log n) with index |
| Storage size | ~1KB per 10 tx | ~1KB per 100 tx |

## Support

If you encounter issues during migration:

1. Check logs: `tail -f logs/bot.log`
2. Verify database: `sqlite3 data/bot.db`
3. Test with fresh install
4. Review this guide
5. Check GitHub issues

## Next Steps

After successful migration:

1. ✅ Test all commands
2. ✅ Monitor logs for errors
3. ✅ Backup database regularly
4. ✅ Update documentation
5. ✅ Train users on new features

---

**Migration Support:** v1.0 → v2.0  
**Estimated Time:** 10-15 minutes  
**Difficulty:** Easy  
**Data Loss Risk:** Low (with backup)
