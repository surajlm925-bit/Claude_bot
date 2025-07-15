"""
Unit tests for services
"""
import pytest
from unittest.mock import patch, MagicMock
from src.services.ai_service import AIService
from src.services.category_detector import CategoryDetector

class TestAIService:
    @pytest.fixture
    def ai_service(self):
        with patch('src.services.ai_service.genai.configure'):
            with patch('src.services.ai_service.genai.GenerativeModel'):
                return AIService()
    
    def test_generate_av_prompt(self, ai_service):
        """Test AV prompt generation"""
        prompt = ai_service.generate_av_prompt("politics", "test content")
        assert "politics" in prompt
        assert "test content" in prompt
        assert "ಕನ್ನಡ" in prompt
    
    @patch('src.services.ai_service.genai.GenerativeModel')
    def test_generate_content_success(self, mock_model, ai_service):
        """Test successful content generation"""
        mock_response = MagicMock()
        mock_response.text = "Generated content"
        mock_model.return_value.generate_content.return_value = mock_response
        
        result = ai_service.generate_content("test prompt")
        assert result == "Generated content"
    
    @patch('src.services.ai_service.genai.GenerativeModel')
    def test_generate_content_error(self, mock_model, ai_service):
        """Test content generation error handling"""
        mock_model.return_value.generate_content.side_effect = Exception("API Error")
        
        result = ai_service.generate_content("test prompt")
        assert "ತಾತ್ಕಾಲಿಕ ತೊಂದರೆ" in result

class TestCategoryDetector:
    @pytest.fixture
    def category_detector(self):
        return CategoryDetector()
    
    def test_user_category_provided(self, category_detector):
        """Test when user provides category"""
        result = category_detector.detect_category("sports", "any content")
        assert result == "sports"
    
    def test_politics_detection(self, category_detector):
        """Test politics category detection"""
        content = "ರಾಜಕೀಯ ಪಕ್ಷದ ಸಭೆ"
        result = category_detector.detect_category("", content)
        assert result == "politics"
    
    def test_default_category(self, category_detector):
        """Test default category for unknown content"""
        content = "unknown content"
        result = category_detector.detect_category("", content)
        assert result == "general"