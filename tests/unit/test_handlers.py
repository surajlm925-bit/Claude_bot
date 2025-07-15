"""
Unit tests for handlers
"""
import pytest
from unittest.mock import patch, MagicMock
from src.handlers.start_handler import StartHandler
from src.handlers.news_handler import NewsHandler
from src.config.constants import START, NEWS_CONTENT

class TestStartHandler:
    @pytest.fixture
    def start_handler(self):
        return StartHandler()
    
    @pytest.mark.asyncio
    async def test_start_command(self, start_handler, mock_update, mock_context):
        """Test /start command"""
        result = await start_handler.start(mock_update, mock_context)
        assert result == START
        assert mock_context.user_data == {}
        mock_update.message.reply_text.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_menu_choice_news(self, start_handler, mock_update, mock_context):
        """Test news menu selection"""
        mock_update.message.text = "📝 ಸುದ್ದಿ ಸ್ಕ್ರಿಪ್ಟ್ ಪ್ರಾರಂಭಿಸಿ"
        result = await start_handler.menu_choice(mock_update, mock_context)
        assert result == NEWS_CONTENT
        mock_update.message.reply_text.assert_called_once()
    
    def test_normalize_input(self, start_handler):
        """Test input normalization"""
        assert start_handler.normalize_input("  TEST  ") == "test"
        assert start_handler.normalize_input("Test") == "test"

class TestNewsHandler:
    @pytest.fixture
    def news_handler(self):
        return NewsHandler()
    
    @pytest.mark.asyncio
    @patch('src.handlers.news_handler.AIService')
    @patch('src.handlers.news_handler.CategoryDetector')
    @patch('src.handlers.news_handler.FileManager')
    async def test_handle_news_content(self, mock_file_manager, mock_category_detector, 
                                     mock_ai_service, news_handler, mock_update, 
                                     mock_context, sample_news_content):
        """Test news content handling"""
        # Setup mocks
        mock_update.message.text = sample_news_content
        mock_category_detector.return_value.detect_category.return_value = "politics"
        mock_ai_service.return_value.generate_content.return_value = "Generated content"
        mock_file_manager.return_value.assemble_output_file.return_value = "/tmp/test.txt"
        
        # Create a test file
        with open("/tmp/test.txt", "w") as f:
            f.write("test content")
        
        result = await news_handler.handle_news_content(mock_update, mock_context)
        
        # Verify calls
        mock_update.message.reply_chat_action.assert_called_once_with(action="typing")
        mock_context.bot.send_document.assert_called_once()
        
        # Cleanup
        import os
        if os.path.exists("/tmp/test.txt"):
            os.remove("/tmp/test.txt")