"""Tests for BalanceService"""

import pytest
import tempfile
from pathlib import Path
from bot.models.database import Database, init_database
from bot.services.balance_service import BalanceService


@pytest.fixture
def temp_db():
    """Create temporary database for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        init_database(db)
        yield db
        db.close()


@pytest.fixture
def balance_service(temp_db):
    """Create balance service with temp database"""
    return BalanceService(temp_db)


class TestBalanceService:
    """Test BalanceService"""
    
    def test_transfer_success(self, balance_service):
        result = balance_service.transfer("person_a", "person_b", 100.0)
        assert result.success is True
        assert result.transaction is not None
        assert balance_service.get_balance("person_a") == 900.0
        assert balance_service.get_balance("person_b") == 1100.0
    
    def test_transfer_insufficient_funds(self, balance_service):
        result = balance_service.transfer("person_a", "person_b", 2000.0)
        assert result.success is False
        assert "Insufficient funds" in result.message
        assert balance_service.get_balance("person_a") == 1000.0
    
    def test_transfer_negative_amount(self, balance_service):
        result = balance_service.transfer("person_a", "person_b", -50.0)
        assert result.success is False
        assert "positive" in result.message.lower()
    
    def test_transfer_same_user(self, balance_service):
        result = balance_service.transfer("person_a", "person_a", 50.0)
        assert result.success is False
        assert "same user" in result.message.lower()
    
    def test_transfer_nonexistent_user(self, balance_service):
        result = balance_service.transfer("person_a", "person_z", 50.0)
        assert result.success is False
        assert "not found" in result.message.lower()
    
    def test_get_all_balances(self, balance_service):
        balance_text = balance_service.get_all_balances()
        assert "Person A" in balance_text
        assert "Person B" in balance_text
        assert "$1000.00" in balance_text
    
    def test_transaction_history(self, balance_service):
        balance_service.transfer("person_a", "person_b", 100.0)
        balance_service.transfer("person_b", "person_a", 50.0)
        
        history = balance_service.get_transaction_history()
        assert "Recent Transactions" in history
        assert "$100.00" in history
        assert "$50.00" in history
    
    def test_reset_all_balances(self, balance_service):
        balance_service.transfer("person_a", "person_b", 100.0)
        balance_service.reset_all_balances(500.0)
        
        assert balance_service.get_balance("person_a") == 500.0
        assert balance_service.get_balance("person_b") == 500.0
        
        history = balance_service.get_transaction_history()
        assert "No transactions" in history
    
    def test_multiple_transfers(self, balance_service):
        balance_service.transfer("person_a", "person_b", 100.0)
        balance_service.transfer("person_a", "person_b", 200.0)
        balance_service.transfer("person_b", "person_a", 50.0)
        
        assert balance_service.get_balance("person_a") == 750.0
        assert balance_service.get_balance("person_b") == 1250.0
