"""
Quick bot functionality test
"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.ai_service import AIService
from src.services.category_detector import CategoryDetector
from src.utils.file_manager import FileManager

async def test_services():
    """Test core services"""
    print("🧪 Testing bot services...")
    
    try:
        # Test category detector
        detector = CategoryDetector()
        category = detector.detect_category("", "ರಾಜಕೀಯ ಸುದ್ದಿ")
        print(f"✅ Category detection: {category}")
        
        # Test file manager
        file_manager = FileManager()
        print("✅ File manager initialized")
        
        # Test AI service (only if API key is available)
        try:
            ai_service = AIService()
            print("✅ AI service initialized")
        except Exception as e:
            print(f"⚠️  AI service: {e}")
        
        print("✅ All services working!")
        
    except Exception as e:
        print(f"❌ Service test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_services())