"""
Unit tests for segment service
"""
import pytest
from unittest.mock import patch, MagicMock
from src.services.segment_service import SegmentService

class TestSegmentService:
    @pytest.fixture
    def segment_service(self):
        return SegmentService()
    
    def test_classify_topic_type_factual(self, segment_service):
        """Test factual topic classification"""
        topic = "ಇಂದಿನ ರಾಜಕೀಯ ಸುದ್ದಿ"
        result = segment_service.classify_topic_type(topic)
        assert result == "factual"
    
    def test_classify_topic_type_general(self, segment_service):
        """Test general topic classification"""
        topic = "ಯೋಗದ ಪ್ರಯೋಜನಗಳು"
        result = segment_service.classify_topic_type(topic)
        assert result == "general"
    
    def test_calculate_content_needs_short(self, segment_service):
        """Test content calculation for short duration"""
        result = segment_service.calculate_content_needs(2)
        assert result["total_words"] == 300
        assert result["sections"] == 2
        assert result["detail"] == "brief"
    
    def test_calculate_content_needs_long(self, segment_service):
        """Test content calculation for long duration"""
        result = segment_service.calculate_content_needs(15)
        assert result["total_words"] == 2250
        assert result["sections"] == 5
        assert result["detail"] == "comprehensive"
    
    @patch('src.services.segment_service.requests.get')
    def test_search_duckduckgo_success(self, mock_get, segment_service):
        """Test successful web search"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'<html><body></body></html>'
        mock_get.return_value = mock_response
        
        result = segment_service.search_duckduckgo("test topic")
        assert isinstance(result, str)
    
    @patch('src.services.segment_service.requests.get')
    def test_search_duckduckgo_failure(self, mock_get, segment_service):
        """Test web search failure handling"""
        mock_get.side_effect = Exception("Network error")
        
        result = segment_service.search_duckduckgo("test topic")
        assert result == ""
    
    @pytest.mark.asyncio
    @patch('src.services.segment_service.SegmentService.ai_service')
    async def test_generate_custom_segment(self, mock_ai_service, segment_service):
        """Test custom segment generation"""
        user_prefs = {
            'topic': 'Technology',
            'content_type': '📚 ಸಾಮಾನ್ಯ ಜ್ಞಾನ/ಶಿಕ್ಷಣ',
            'info_source': '🧠 ಕೇವಲ AI ಜ್ಞಾನ',
            'detail_level': '📋 ಮಧ್ಯಮ ವಿವರಣೆ',
            'presentation_style': '📺 ಟಿವಿ ನ್ಯೂಸ್ ಶೈಲಿ',
            'content_richness': '📝 ಉದಾಹರಣೆಗಳೊಂದಿಗೆ'
        }
        
        mock_ai_service.generate_content.return_value = "Generated segment content"
        
        segment_text, category, sources = await segment_service.generate_custom_segment(user_prefs, 5)
        
        assert segment_text == "Generated segment content"
        assert isinstance(category, str)
        assert isinstance(sources, str)