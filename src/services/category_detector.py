"""
Category Detection Service (migrated from your category_detector.py)
"""
import logging

logger = logging.getLogger(__name__)

class CategoryDetector:
    def detect_category(self, user_category: str, content_text: str) -> str:
        """
        Uses the user-provided category as-is if given, else falls back to keyword detection.
        """
        if user_category and user_category.strip() != "":
            return user_category.strip()

        # Fallback: keyword-based detection
        text_lower = content_text.lower()

        if "ರಾಜಕೀಯ" in text_lower or "ಸಿಎಂ" in text_lower or "ಪಕ್ಷ" in text_lower:
            return "politics"
        if "ಅಪಘಾತ" in text_lower or "ಸಾವು" in text_lower or "ಗಾಯ" in text_lower:
            return "accidents"
        if "ಕೊಲೆ" in text_lower or "ಅಪರಾಧ" in text_lower or "ಪೊಲೀಸ್" in text_lower:
            return "crime"
        if "ಸಿನಿಮಾ" in text_lower or "ನಟ" in text_lower or "ಚಿತ್ರ" in text_lower:
            return "cinema"
        if "ನೀರು" in text_lower or "ರಸ್ತೆ" in text_lower or "ಆಸ್ಪತ್ರೆ" in text_lower:
            return "infrastructure"
        if "ಹಬ್ಬ" in text_lower or "ಸಂಭ್ರಮ" in text_lower or "ಕಾರ್ಯಕ್ರಮ" in text_lower:
            return "culture"
        if "ಧಾರ್ಮಿಕ" in text_lower or "ಪೂಜೆ" in text_lower or "ಆಧ್ಯಾತ್ಮಿಕ" in text_lower:
            return "spiritual"
        if "ಆರೋಗ್ಯ" in text_lower or "ಹಾಸ್ಪಟಲ್" in text_lower:
            return "health"
        if "ಬ್ಯಾಂಕ್" in text_lower or "ಹೂಡಿಕೆ" in text_lower:
            return "business"

        return "general"