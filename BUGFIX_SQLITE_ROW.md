# Bug Fix: sqlite3.Row AttributeError

## Issue

When running transfers, the bot was throwing an error:
```
❌ Transfer failed: 'sqlite3.Row' object has no attribute 'get'
```

## Root Cause

The `sqlite3.Row` object doesn't support the `.get()` method like a regular Python dictionary. The code was trying to use `row.get('from_user_name')` which caused an `AttributeError`.

## Files Fixed

### 1. `bot/services/transaction_service.py`

**Problem:**
```python
from_user_name=row.get('from_user_name'),  # ❌ Doesn't work with sqlite3.Row
to_user_name=row.get('to_user_name')       # ❌ Doesn't work with sqlite3.Row
```

**Solution:**
```python
@staticmethod
def _get_row_value(row, key: str, default=None):
    """Safely get value from sqlite3.Row object"""
    try:
        return row[key]
    except (KeyError, IndexError):
        return default

def _row_to_transaction(self, row) -> Transaction:
    """Convert database row to Transaction object"""
    return Transaction(
        id=row['id'],
        from_user_id=row['from_user_id'],
        to_user_id=row['to_user_id'],
        amount=row['amount'],
        balance_from=row['balance_from'],
        balance_to=row['balance_to'],
        created_at=row['created_at'],
        from_user_name=self._get_row_value(row, 'from_user_name'),  # ✅ Safe access
        to_user_name=self._get_row_value(row, 'to_user_name')       # ✅ Safe access
    )
```

### 2. `bot/models/transaction.py`

**Additional Issue Found:**
SQLite returns timestamps as strings, not datetime objects.

**Problem:**
```python
created_at: Optional[datetime] = None  # ❌ SQLite returns strings
timestamp = self.created_at.strftime("%Y-%m-%d %H:%M:%S")  # ❌ Fails on strings
```

**Solution:**
```python
created_at: Optional[Union[datetime, str]] = None  # ✅ Accept both types

def format_display(self) -> str:
    """Format transaction for display"""
    # Handle both datetime objects and string timestamps from SQLite
    if self.created_at:
        if isinstance(self.created_at, str):
            timestamp = self.created_at  # ✅ Use string directly
        else:
            timestamp = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    else:
        timestamp = "N/A"
    
    return (
        f"💸 ${self.amount:.2f} | {from_name} → {to_name}\n"
        f"   {timestamp}"
    )
```

## Testing

All tests pass successfully:

```bash
$ pytest tests/ -v
================ test session starts =================
collected 17 items

tests/test_balance_service.py::TestBalanceService::test_transfer_success PASSED
tests/test_balance_service.py::TestBalanceService::test_transfer_insufficient_funds PASSED
tests/test_balance_service.py::TestBalanceService::test_transfer_negative_amount PASSED
tests/test_balance_service.py::TestBalanceService::test_transfer_same_user PASSED
tests/test_balance_service.py::TestBalanceService::test_transfer_nonexistent_user PASSED
tests/test_balance_service.py::TestBalanceService::test_get_all_balances PASSED
tests/test_balance_service.py::TestBalanceService::test_transaction_history PASSED
tests/test_balance_service.py::TestBalanceService::test_reset_all_balances PASSED
tests/test_balance_service.py::TestBalanceService::test_multiple_transfers PASSED
tests/test_user_service.py::TestUserService::test_get_by_name PASSED
tests/test_user_service.py::TestUserService::test_get_by_id PASSED
tests/test_user_service.py::TestUserService::test_get_all PASSED
tests/test_user_service.py::TestUserService::test_create_user PASSED
tests/test_user_service.py::TestUserService::test_update_balance PASSED
tests/test_user_service.py::TestUserService::test_update_balance_negative_fails PASSED
tests/test_user_service.py::TestUserService::test_reset_all_balances PASSED
tests/test_user_service.py::TestUserService::test_delete_user PASSED

================= 17 passed in 1.06s =================
```

## Verification

Created and ran a test script that verified:
1. ✅ Transaction creation works
2. ✅ User names are properly retrieved
3. ✅ Transaction history displays correctly
4. ✅ No sqlite3.Row errors
5. ✅ Timestamps display correctly

## Summary

- **Issue:** `sqlite3.Row` doesn't support `.get()` method
- **Fix:** Created helper method `_get_row_value()` for safe access
- **Bonus Fix:** Handle both datetime and string timestamps from SQLite
- **Status:** ✅ Fixed and tested
- **Tests:** All 17 tests passing

## How to Verify

Run the bot and try a transfer:
```bash
python run.py
```

Then in Telegram:
1. Send `/transfer`
2. Select direction
3. Enter amount
4. Should see: "✅ Transfer successful!"

Or run tests:
```bash
pytest tests/ -v
```
