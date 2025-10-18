import pytest
from unittest.mock import Mock, patch
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
        mock_blacklist.created_at = "2025-10-13T10:30:00"
        
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

