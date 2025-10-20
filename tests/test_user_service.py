"""Tests for UserService"""

import pytest
import tempfile
from pathlib import Path
from bot.models.database import Database, init_database
from bot.services.user_service import UserService


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
def user_service(temp_db):
    """Create user service with temp database"""
    return UserService(temp_db)


class TestUserService:
    """Test UserService"""
    
    def test_get_by_name(self, user_service):
        user = user_service.get_by_name("person_a")
        assert user is not None
        assert user.name == "person_a"
        assert user.balance == 1000.0
    
    def test_get_by_id(self, user_service):
        user = user_service.get_by_name("person_a")
        user_by_id = user_service.get_by_id(user.id)
        assert user_by_id.name == "person_a"
    
    def test_get_all(self, user_service):
        users = user_service.get_all()
        assert len(users) == 2
        assert any(u.name == "person_a" for u in users)
        assert any(u.name == "person_b" for u in users)
    
    def test_create_user(self, user_service):
        new_user = user_service.create("person_c", 500.0)
        assert new_user.name == "person_c"
        assert new_user.balance == 500.0
        assert new_user.id is not None
    
    def test_update_balance(self, user_service):
        user = user_service.get_by_name("person_a")
        success = user_service.update_balance(user.id, 750.0)
        assert success is True
        
        updated_user = user_service.get_by_id(user.id)
        assert updated_user.balance == 750.0
    
    def test_update_balance_negative_fails(self, user_service):
        user = user_service.get_by_name("person_a")
        with pytest.raises(ValueError):
            user_service.update_balance(user.id, -100.0)
    
    def test_reset_all_balances(self, user_service):
        user_service.reset_all_balances(2000.0)
        users = user_service.get_all()
        for user in users:
            assert user.balance == 2000.0
    
    def test_delete_user(self, user_service):
        user = user_service.create("temp_user", 100.0)
        user_service.delete(user.id)
        deleted_user = user_service.get_by_id(user.id)
        assert deleted_user is None
