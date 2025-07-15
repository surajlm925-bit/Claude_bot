"""
Pytest configuration and fixtures
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, Message, Chat, User
from telegram.ext import ContextTypes

@pytest.fixture
def mock_update():
    """Create a mock Update object"""
    update = AsyncMock(spec=Update)
    update.message = AsyncMock(spec=Message)
    update.message.chat = MagicMock(spec=Chat)
    update.message.chat.id = 123456
    update.message.from_user = MagicMock(spec=User)
    update.message.from_user.id = 789
    update.message.from_user.first_name = "Test User"
    update.message.text = "test message"
    update.message.reply_text = AsyncMock()
    update.message.reply_chat_action = AsyncMock()
    return update

@pytest.fixture
def mock_context():
    """Create a mock Context object"""
    context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    context.user_data = {}
    context.bot = AsyncMock()
    context.bot.send_document = AsyncMock()
    context.bot.get_file = AsyncMock()
    return context

@pytest.fixture
def sample_news_content():
    """Sample Kannada news content for testing"""
    return "ಬೆಂಗಳೂರಿನ ಮಹತ್ವದ ಸುದ್ದಿ. ಇಂದು ರಾಜ್ಯ ಸರ್ಕಾರ ಹೊಸ ನೀತಿ ಪ್ರಕಟಿಸಿದೆ."