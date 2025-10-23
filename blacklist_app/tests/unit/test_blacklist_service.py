import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from src.services.blacklist_service import BlacklistService
from src.models.errors import ConflictError


class TestBlacklistService:
    """
    Unit tests for BlacklistService.
    """
    
    def setup_method(self):
        """Setup test fixtures."""
        self.service = BlacklistService()
    
    @patch('src.services.blacklist_service.BlacklistRepository')
    def test_add_to_blacklist_success(self, mock_repo_class):
        """Test successfully adding an email to blacklist."""
        # Setup
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        
        mock_blacklist = Mock()
        mock_blacklist.id = "test-id"
        mock_blacklist.email = "test@example.com"
        mock_blacklist.created_at = datetime(2025, 10, 13, 10, 30, 0)
        
        mock_repo.create.return_value = mock_blacklist
        
        # Execute
        service = BlacklistService()
        result = service.add_to_blacklist(
            email="test@example.com",
            app_uuid="app-uuid",
            blocked_reason="Test reason",
            ip_address="127.0.0.1"
        )
        
        # Assert
        assert "message" in result
        assert "test@example.com" in result["message"]
        assert result["email"] == "test@example.com"
        assert result["id"] == "test-id"
        assert "created_at" in result
        
        # Verify repository was called with correct data
        call_args = mock_repo.create.call_args[0][0]
        assert call_args["email"] == "test@example.com"
        assert call_args["app_uuid"] == "app-uuid"
        assert call_args["blocked_reason"] == "Test reason"
        assert call_args["ip_address"] == "127.0.0.1"
        assert "id" in call_args
    
    @patch('src.services.blacklist_service.BlacklistRepository')
    def test_add_to_blacklist_with_empty_blocked_reason(self, mock_repo_class):
        """Test adding an email to blacklist with empty blocked reason."""
        # Setup
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        
        mock_blacklist = Mock()
        mock_blacklist.id = "test-id"
        mock_blacklist.email = "test@example.com"
        mock_blacklist.created_at = datetime(2025, 10, 13, 10, 30, 0)
        
        mock_repo.create.return_value = mock_blacklist
        
        # Execute
        service = BlacklistService()
        result = service.add_to_blacklist(
            email="test@example.com",
            app_uuid="app-uuid",
            blocked_reason="",
            ip_address="127.0.0.1"
        )
        
        # Assert
        assert result["email"] == "test@example.com"
        call_args = mock_repo.create.call_args[0][0]
        assert call_args["blocked_reason"] == ""
    
    @patch('src.services.blacklist_service.BlacklistRepository')
    def test_add_to_blacklist_duplicate_email(self, mock_repo_class):
        """Test adding a duplicate email raises ConflictError."""
        # Setup
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        mock_repo.create.side_effect = ConflictError("Email test@example.com is already in the blacklist")
        
        # Execute & Assert
        service = BlacklistService()
        with pytest.raises(ConflictError) as exc_info:
            service.add_to_blacklist(
                email="test@example.com",
                app_uuid="app-uuid",
                blocked_reason="Test reason",
                ip_address="127.0.0.1"
            )
        
        assert "already in the blacklist" in str(exc_info.value)
    
    @patch('src.services.blacklist_service.BlacklistRepository')
    def test_add_to_blacklist_generates_unique_id(self, mock_repo_class):
        """Test that add_to_blacklist generates a unique UUID for each entry."""
        # Setup
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        
        mock_blacklist = Mock()
        mock_blacklist.id = "generated-uuid"
        mock_blacklist.email = "test@example.com"
        mock_blacklist.created_at = datetime(2025, 10, 13, 10, 30, 0)
        
        mock_repo.create.return_value = mock_blacklist
        
        # Execute
        service = BlacklistService()
        service.add_to_blacklist(
            email="test@example.com",
            app_uuid="app-uuid",
            blocked_reason="Test reason",
            ip_address="127.0.0.1"
        )
        
        # Assert - verify that an ID was generated
        call_args = mock_repo.create.call_args[0][0]
        assert "id" in call_args
        assert call_args["id"] is not None
        assert len(call_args["id"]) > 0
    
    @patch('src.services.blacklist_service.BlacklistRepository')
    def test_add_to_blacklist_with_special_characters_in_email(self, mock_repo_class):
        """Test adding an email with special characters."""
        # Setup
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        
        special_email = "test+tag@example.co.uk"
        mock_blacklist = Mock()
        mock_blacklist.id = "test-id"
        mock_blacklist.email = special_email
        mock_blacklist.created_at = datetime(2025, 10, 13, 10, 30, 0)
        
        mock_repo.create.return_value = mock_blacklist
        
        # Execute
        service = BlacklistService()
        result = service.add_to_blacklist(
            email=special_email,
            app_uuid="app-uuid",
            blocked_reason="Test reason",
            ip_address="192.168.1.1"
        )
        
        # Assert
        assert result["email"] == special_email
        call_args = mock_repo.create.call_args[0][0]
        assert call_args["email"] == special_email
    
    @patch('src.services.blacklist_service.BlacklistRepository')
    def test_check_blacklist_found(self, mock_repo_class):
        """Test checking a blacklisted email."""
        # Setup
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        
        mock_blacklist = Mock()
        mock_blacklist.email = "test@example.com"
        mock_blacklist.blocked_reason = "Spam"
        
        mock_repo.get_by_email.return_value = mock_blacklist
        
        # Execute
        service = BlacklistService()
        result = service.check_blacklist("test@example.com")
        
        # Assert
        assert result["is_blacklisted"] is True
        assert result["email"] == "test@example.com"
        assert result["blocked_reason"] == "Spam"
        mock_repo.get_by_email.assert_called_once_with("test@example.com")
    
    @patch('src.services.blacklist_service.BlacklistRepository')
    def test_check_blacklist_not_found(self, mock_repo_class):
        """Test checking a non-blacklisted email."""
        # Setup
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        mock_repo.get_by_email.return_value = None
        
        # Execute
        service = BlacklistService()
        result = service.check_blacklist("test@example.com")
        
        # Assert
        assert result["is_blacklisted"] is False
        assert result["email"] == "test@example.com"
        assert result["blocked_reason"] is None
        mock_repo.get_by_email.assert_called_once_with("test@example.com")
    
    @patch('src.services.blacklist_service.BlacklistRepository')
    def test_check_blacklist_with_empty_blocked_reason(self, mock_repo_class):
        """Test checking a blacklisted email with empty blocked reason."""
        # Setup
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        
        mock_blacklist = Mock()
        mock_blacklist.email = "test@example.com"
        mock_blacklist.blocked_reason = ""
        
        mock_repo.get_by_email.return_value = mock_blacklist
        
        # Execute
        service = BlacklistService()
        result = service.check_blacklist("test@example.com")
        
        # Assert
        assert result["is_blacklisted"] is True
        assert result["email"] == "test@example.com"
        assert result["blocked_reason"] == ""
    
    @patch('src.services.blacklist_service.BlacklistRepository')
    def test_check_blacklist_with_none_blocked_reason(self, mock_repo_class):
        """Test checking a blacklisted email with None blocked reason."""
        # Setup
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        
        mock_blacklist = Mock()
        mock_blacklist.email = "test@example.com"
        mock_blacklist.blocked_reason = None
        
        mock_repo.get_by_email.return_value = mock_blacklist
        
        # Execute
        service = BlacklistService()
        result = service.check_blacklist("test@example.com")
        
        # Assert
        assert result["is_blacklisted"] is True
        assert result["email"] == "test@example.com"
        assert result["blocked_reason"] is None
    
    @patch('src.services.blacklist_service.BlacklistRepository')
    def test_check_blacklist_case_sensitive(self, mock_repo_class):
        """Test that check_blacklist is case-sensitive (passes exact email to repository)."""
        # Setup
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        mock_repo.get_by_email.return_value = None
        
        # Execute
        service = BlacklistService()
        service.check_blacklist("Test@Example.COM")
        
        # Assert - verify exact email is passed to repository
        mock_repo.get_by_email.assert_called_once_with("Test@Example.COM")
    
    @patch('src.services.blacklist_service.BlacklistRepository')
    def test_add_to_blacklist_with_long_blocked_reason(self, mock_repo_class):
        """Test adding an email with a long blocked reason."""
        # Setup
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        
        long_reason = "A" * 500  # 500 character reason
        mock_blacklist = Mock()
        mock_blacklist.id = "test-id"
        mock_blacklist.email = "test@example.com"
        mock_blacklist.created_at = datetime(2025, 10, 13, 10, 30, 0)
        
        mock_repo.create.return_value = mock_blacklist
        
        # Execute
        service = BlacklistService()
        result = service.add_to_blacklist(
            email="test@example.com",
            app_uuid="app-uuid",
            blocked_reason=long_reason,
            ip_address="127.0.0.1"
        )
        
        # Assert
        assert result["email"] == "test@example.com"
        call_args = mock_repo.create.call_args[0][0]
        assert call_args["blocked_reason"] == long_reason
    
    @patch('src.services.blacklist_service.BlacklistRepository')
    def test_add_to_blacklist_return_structure(self, mock_repo_class):
        """Test that add_to_blacklist returns the correct structure."""
        # Setup
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        
        mock_blacklist = Mock()
        mock_blacklist.id = "test-id-123"
        mock_blacklist.email = "user@domain.com"
        mock_blacklist.created_at = datetime(2025, 10, 13, 15, 45, 30)
        
        mock_repo.create.return_value = mock_blacklist
        
        # Execute
        service = BlacklistService()
        result = service.add_to_blacklist(
            email="user@domain.com",
            app_uuid="app-uuid-456",
            blocked_reason="Suspicious activity",
            ip_address="10.0.0.1"
        )
        
        # Assert - verify all required fields are present
        assert "message" in result
        assert "id" in result
        assert "email" in result
        assert "created_at" in result
        assert result["id"] == "test-id-123"
        assert result["email"] == "user@domain.com"
        assert isinstance(result["created_at"], str)
    
    @patch('src.services.blacklist_service.BlacklistRepository')
    def test_check_blacklist_return_structure(self, mock_repo_class):
        """Test that check_blacklist returns the correct structure."""
        # Setup
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo
        mock_repo.get_by_email.return_value = None
        
        # Execute
        service = BlacklistService()
        result = service.check_blacklist("test@example.com")
        
        # Assert - verify all required fields are present
        assert "is_blacklisted" in result
        assert "email" in result
        assert "blocked_reason" in result
        assert isinstance(result["is_blacklisted"], bool)

