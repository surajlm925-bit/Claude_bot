"""
Advanced Segment Generation Service (migrated from segment.py)
"""
import requests
import urllib.parse
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, Tuple
from src.services.ai_service import AIService
from src.services.category_detector import CategoryDetector
from src.config.constants import TRUSTED_SOURCES
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SegmentService:
    def __init__(self):
        self.ai_service = AIService()
        self.category_detector = CategoryDetector()
        self.logger = logger
    
    def classify_topic_type(self, topic: str) -> str:
        """Determine if topic needs fact-checking or can use general knowledge"""
        topic_lower = topic.lower()
        
        # Topics that need current information and fact-checking
        factual_keywords = [
            "ಸದ್ಯದ", "ಇತ್ತೀಚಿನ", "ಇಂದಿನ", "ಈಗಿನ", "ಪ್ರಸ್ತುತ", "ಸುದ್ದಿ",
            "ರಾಜಕೀಯ", "ಸರ್ಕಾರ", "ಚುನಾವಣೆ", "ಸಿಎಂ", "ಪ್ರಧಾನಿ", "ಪಕ್ಷ",
            "ಘಟನೆ", "ಕ್ರೀಡಾ ಸುದ್ದಿ", "ಪಂದ್ಯ ಫಲಿತಾಂಶ", "ಮುಖ್ಯಮಂತ್ರಿ"
        ]
        
        # Check if needs fact-checking
        if any(keyword in topic_lower for keyword in factual_keywords):
            return "factual"
        return "general"

    def calculate_content_needs(self, duration_minutes: int) -> dict:
        """Calculate how much content is needed for the duration"""
        # Kannada speaking speed: 150 words per minute
        total_words = duration_minutes * 150
        
        if duration_minutes <= 2:
            return {"total_words": total_words, "sections": 2, "detail": "brief"}
        elif duration_minutes <= 5:
            return {"total_words": total_words, "sections": 3, "detail": "moderate"}
        elif duration_minutes <= 10:
            return {"total_words": total_words, "sections": 4, "detail": "detailed"}
        else:
            return {"total_words": total_words, "sections": max(5, duration_minutes//3), "detail": "comprehensive"}

    def search_duckduckgo(self, topic: str) -> str:
        """Search for current information if needed"""
        try:
            site_filters = " OR ".join([f"site:{source}" for source in TRUSTED_SOURCES[:5]])
            search_query = f"{topic} India news ({site_filters})"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(search_query)}"
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                results = []
                
                for result in soup.find_all('div', class_='result__body')[:3]:
                    title_elem = result.find('a', class_='result__a')
                    snippet_elem = result.find('a', class_='result__snippet')
                    
                    if title_elem and snippet_elem:
                        title = title_elem.get_text().strip()
                        snippet = snippet_elem.get_text().strip()
                        url = title_elem.get('href', '')
                        
                        if any(source in url for source in TRUSTED_SOURCES):
                            results.append(f"Title: {title}\nSnippet: {snippet}\nSource: {url}\n")
                
                return "\n".join(results) if results else ""
            return ""
            
        except Exception as e:
            self.logger.error(f"Search error: {e}")
            return ""

    def create_enhanced_prompt(self, topic: str, duration: int, topic_type: str, 
                             content_needs: dict, web_results: str = "") -> str:
        """Create the enhanced prompt based on topic type and duration"""
        
        total_words = content_needs["total_words"]
        sections = content_needs["sections"]
        detail_level = content_needs["detail"]
        
        # Different strategies for different topic types
        if topic_type == "factual":
            content_guidance = f"""
📊 ವಿಷಯ ಪ್ರಕಾರ: ಸತ್ಯ-ಪರಿಶೀಲನೆ ಅಗತ್ಯ (ಸದ್ಯದ ಸುದ್ದಿ)

⚠️ ಮಹತ್ವದ ನಿಯಮಗಳು:
• ಕೇವಲ ಕೆಳಗಿನ ವೆಬ್ ಸರ್ಚ್ ಮಾಹಿತಿಯನ್ನು ಮಾತ್ರ ಬಳಸಿ
• "ವರದಿಗಳ ಪ್ರಕಾರ", "ಮೂಲಗಳ ಪ್ರಕಾರ" ಎಂಬ ಪದಗಳನ್ನು ಬಳಸಿ
• ದಿನಾಂಕಗಳು ಮತ್ತು ಅಂಕಿಅಂಶಗಳನ್ನು ಸೇರಿಸಿ

🔍 ವೆಬ್ ಸರ್ಚ್ ಮಾಹಿತಿ:
{web_results if web_results else "ವೆಬ್ ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ - ಸಾಮಾನ್ಯ ಮಾಹಿತಿ ಮಾತ್ರ ನೀಡಿ"}
"""
        else:
            content_guidance = f"""
📚 ವಿಷಯ ಪ್ರಕಾರ: ಸಾಮಾನ್ಯ ಜ್ಞಾನ/ಶಿಕ್ಷಣ/ಮನರಂಜನೆ

✅ ನಿಮಗೆ ಸಂಪೂರ್ಣ ಸ್ವಾತಂತ್ರ್ಯ:
• ನಿಮ್ಮ ಸಂಪೂರ್ಣ ಜ್ಞಾನವನ್ನು ಬಳಸಿ
• ವಿಸ್ತೃತ ವಿವರಣೆಗಳು, ಉದಾಹರಣೆಗಳು, ಕಥೆಗಳನ್ನು ಸೇರಿಸಿ
• ಐತಿಹಾಸಿಕ ಸಂದರ್ಭ, ವೈಜ್ಞಾನಿಕ ವಿವರಣೆಗಳನ್ನು ನೀಡಿ
• ಆಸಕ್ತಿದಾಯಕ ಮತ್ತು ಶಿಕ್ಷಣಾತ್ಮಕವಾಗಿ ಮಾಡಿ

💡 ಹೆಚ್ಚುವರಿ ಮಾಹಿತಿ:
{web_results if web_results else "ನಿಮ್ಮ ಜ್ಞಾನ ಆಧಾರದಲ್ಲಿ ಸಂಪೂರ್ಣ ಸೆಗ್ಮೆಂಟ್ ರಚಿಸಿ"}
"""

        # Duration-specific instructions
        if duration <= 2:
            duration_guide = "• ಸಂಕ್ಷಿಪ್ತ ಆದರೆ ಪೂರ್ಣ ಮಾಹಿತಿ"
        elif duration <= 5:
            duration_guide = "• ಮಧ್ಯಮ ವಿವರಣೆ ಮತ್ತು ಉದಾಹರಣೆಗಳು"
        elif duration <= 10:
            duration_guide = "• ವಿವರವಾದ ವಿವರಣೆ, ಬಹು ಉದಾಹರಣೆಗಳು"
        else:
            duration_guide = "• ಸಮಗ್ರ ವಿವರಣೆ, ಇತಿಹಾಸ, ಸಂದರ್ಭ, ಅನುಷಂಗಿಕ ವಿಷಯಗಳು"

        return f"""
ನೀವು ಅನುಭವಿ ಕನ್ನಡ ಟಿವಿ ಹೋಸ್ಟ್ ಮತ್ತು ಶಿಕ್ಷಣ ತಜ್ಞ. "{topic}" ವಿಷಯದ ಬಗ್ಗೆ ನಿಖರವಾಗಿ {duration} ನಿಮಿಷಗಳ ಟಿವಿ ಸೆಗ್ಮೆಂಟ್ ರಚಿಸಿ.

{content_guidance}

📏 ಅವಧಿ ಅವಶ್ಯಕತೆಗಳು:
• ನಿಖರವಾಗಿ {duration} ನಿಮಿಷಗಳ ಓದುವ ಸಮಯ (ಸುಮಾರು {total_words} ಪದಗಳು)
• {sections} ಮುಖ್ಯ ವಿಭಾಗಗಳಲ್ಲಿ ವಿಂಗಡಿಸಿ
{duration_guide}

🎯 ಸೆಗ್ಮೆಂಟ್ ರಚನೆ:
1. ಆಕರ್ಷಕ ಪರಿಚಯ (ಪ್ರೇಕ್ಷಕರ ಗಮನ ಸೆಳೆಯಿರಿ)
2. ಮುಖ್ಯ ವಿಷಯ ವಿವರಣೆ
3. ಉದಾಹರಣೆಗಳು ಮತ್ತು ವಿವರಗಳು ({detail_level} ಮಟ್ಟದಲ್ಲಿ)
4. ಪ್ರಭಾವಶಾಲಿ ಮುಕ್ತಾಯ

📝 ಭಾಷಾ ಮಾರ್ಗದರ್ಶನ:
• ಶುದ್ಧ ಕನ್ನಡ, ಸರಳ ಮತ್ತು ಸ್ಪಷ್ಟ
• ಟಿವಿ ಪ್ರೇಕ್ಷಕರಿಗೆ ಸೂಕ್ತ ಶೈಲಿ
• ಪ್ರತಿ ಪ್ಯಾರಾಗ್ರಾಫ್ 30-40 ಸೆಕೆಂಡುಗಳ ಓದುವ ಸಮಯ

⚠️ ಮುಖ್ಯ: ಸೆಗ್ಮೆಂಟ್ ಓದಲು ನಿಖರವಾಗಿ {duration} ನಿಮಿಷಗಳು ಬೇಕಾಗಬೇಕು. ತುಂಬಾ ಚಿಕ್ಕದಾಗಿರಬಾರದು!
"""

    async def generate_custom_segment(self, user_prefs: dict, duration: int) -> Tuple[str, str, str]:
        """Generate segment based on user's 5 interactive answers"""
        try:
            topic = user_prefs.get('topic', '')
            content_type = user_prefs.get('content_type', '')
            info_source = user_prefs.get('info_source', '')
            
            # Determine if web search is needed
            web_results = ""
            should_search = (
                "ಇತ್ತೀಚಿನ ಸುದ್ದಿ" in content_type or
                "ವೆಬ್ ಸರ್ಚ್" in info_source
            )
            
            if should_search:
                self.logger.info(f"Performing web search for user-requested topic: {topic}")
                web_results = self.search_duckduckgo(topic)
            
            # Create custom prompt based on user preferences
            custom_prompt = self.create_interactive_prompt(user_prefs, duration, web_results)
            
            # Generate content
            segment_text = self.ai_service.generate_content(custom_prompt)
            
            # Determine category and sources
            category = self.category_detector.detect_category("", topic)
            
            if web_results:
                sources = "ವೆಬ್ ಸರ್ಚ್ + AI ಕಸ್ಟಮೈಜೇಶನ್"
            else:
                sources = "AI ಜ್ಞಾನ + ಯೂಸರ್ ಪ್ರಿಫರೆನ್ಸ್"
            
            return segment_text, category, sources
            
        except Exception as e:
            self.logger.error(f"Error in custom segment generation: {e}")
            return f"ಕ್ಷಮಿಸಿ, ಕಸ್ಟಮ್ ಸೆಗ್ಮೆಂಟ್ ರಚನೆಯಲ್ಲಿ ದೋಷ: {str(e)}", "error", "N/A"

    def create_interactive_prompt(self, user_prefs: dict, duration: int, web_results: str = "") -> str:
        """Create a highly customized prompt based on user's interactive choices"""
        topic = user_prefs.get('topic', '')
        content_type = user_prefs.get('content_type', '')
        info_source = user_prefs.get('info_source', '')
        detail_level = user_prefs.get('detail_level', '')
        presentation_style = user_prefs.get('presentation_style', '')
        content_richness = user_prefs.get('content_richness', '')
        
        # Calculate words needed
        total_words = duration * 150
        
        # Build content strategy based on user choices
        content_strategy = f"""
🎯 ಕಸ್ಟಮೈಜ್ಡ್ ಸೆಗ್ಮೆಂಟ್ ಸೃಷ್ಟಿ
━━━━━━━━━━━━━━━━━━━━━━━━

👤 ಯೂಸರ್ ಆಯ್ಕೆಗಳು:
• ವಿಷಯ ಪ್ರಕಾರ: {content_type}
• ಮಾಹಿತಿ ಮೂಲ: {info_source}
• ವಿವರ ಮಟ್ಟ: {detail_level}
• ಪ್ರಸ್ತುತಿ ಶೈಲಿ: {presentation_style}
• ವಿಷಯ ಸಮೃದ್ಧಿ: {content_richness}
"""

        # Add web search info if available
        if web_results and "ವೆಬ್ ಸರ್ಚ್" in info_source:
            content_strategy += f"""
🔍 ವೆಬ್ ಸರ್ಚ್ ಫಲಿತಾಂಶಗಳು:
{web_results}

⚠️ ಮೇಲಿನ ವೆಬ್ ಮಾಹಿತಿಯನ್ನು ಬಳಸಿ ಮತ್ತು ಯೂಸರ್ ಆಯ್ಕೆಗಳಿಗೆ ಅನುಗುಣವಾಗಿ ಬರೆಯಿರಿ.
"""
        
        # Content depth instructions based on detail level
        depth_instructions = ""
        if "ಸಂಕ್ಷಿಪ್ತ" in detail_level:
            depth_instructions = "• ಮುಖ್ಯ ಅಂಶಗಳನ್ನು ಮಾತ್ರ ಒಳಗೊಳ್ಳಿ, ಸಂಕ್ಷಿಪ್ತವಾಗಿ ಬರೆಯಿರಿ"
        elif "ಮಧ್ಯಮ" in detail_level:
            depth_instructions = "• ಮುಖ್ಯ ಅಂಶಗಳು + ಕೆಲವು ಉದಾಹರಣೆಗಳನ್ನು ಸೇರಿಸಿ"
        elif "ವಿಸ್ತೃತ" in detail_level:
            depth_instructions = "• ವಿವರವಾದ ವಿವರಣೆ, ಬಹು ಉದಾಹರಣೆಗಳು, ಸಂದರ್ಭ ಮಾಹಿತಿ ಸೇರಿಸಿ"
        else:  # ಸಮಗ್ರ
            depth_instructions = "• ಸಂಪೂರ್ಣ ವಿವರಣೆ, ಇತಿಹಾಸ, ಉದಾಹರಣೆಗಳು, ಕಥೆಗಳು, ಸಂಬಂಧಿತ ವಿಷಯಗಳು"
        
        # Style instructions based on presentation choice
        style_instructions = ""
        if "ಟಿವಿ ನ್ಯೂಸ್" in presentation_style:
            style_instructions = "• ಟಿವಿ ಆಂಕರ್ ಶೈಲಿ, ಔಪಚಾರಿಕ ಟೋನ್, ಸುದ್ದಿ ಫಾರ್ಮ್ಯಾಟ್"
        elif "ರೇಡಿಯೋ" in presentation_style:
            style_instructions = "• ರೇಡಿಯೋ ಶೈಲಿ, ವರ್ಣನಾತ್ಮಕ ಭಾಷೆ, ಆಡಿಯೋ-ಫ್ರೆಂಡ್ಲಿ"
        elif "ಶೈಕ್ಷಣಿಕ" in presentation_style:
            style_instructions = "• ಶಿಕ್ಷಕರ ಶೈಲಿ, ವಿವರಣಾತ್ಮಕ, ಸರಳ ಭಾಷೆ"
        else:  # ಸಂಭಾಷಣಾ
            style_instructions = "• ಸ್ನೇಹಪರ ಟೋನ್, ಸಂವಾದಾತ್ಮಕ, ಪ್ರಶ್ನೆಗಳನ್ನು ಸೇರಿಸಿ"
        
        # Richness instructions
        richness_instructions = ""
        if "ಮುಖ್ಯ ವಿಷಯ ಮಾತ್ರ" in content_richness:
            richness_instructions = "• ಮೂಲ ವಿಷಯಕ್ಕೆ ಸೀಮಿತವಾಗಿರಿ"
        elif "ಉದಾಹರಣೆಗಳೊಂದಿಗೆ" in content_richness:
            richness_instructions = "• ಪ್ರತಿ ಪಾಯಿಂಟ್‌ಗೆ ಉದಾಹರಣೆಗಳನ್ನು ಸೇರಿಸಿ"
        elif "ಕಥೆಗಳು" in content_richness:
            richness_instructions = "• ಆಸಕ್ತಿದಾಯಕ ಕಥೆಗಳು, ಉದಾಹರಣೆಗಳು, ವೈಯಕ್ತಿಕ ಅನುಭವಗಳನ್ನು ಸೇರಿಸಿ"
        else:  # ಸಂವಾದಾತ್ಮಕ
            richness_instructions = "• ಪ್ರೇಕ್ಷಕರೊಂದಿಗೆ ಸಂವಾದ, ಪ್ರಶ್ನೆಗಳು, ಕ್ರಿಯಾಶೀಲ ಭಾಗವಹಿಸುವಿಕೆ"

        return f"""
ನೀವು ಅನುಭವಿ ಕನ್ನಡ ಮಾಧ್ಯಮ ವ್ಯಕ್ತಿತ್ವ. "{topic}" ವಿಷಯದ ಬಗ್ಗೆ ನಿಖರವಾಗಿ {duration} ನಿಮಿಷಗಳ ಸೆಗ್ಮೆಂಟ್ ರಚಿಸಿ.

{content_strategy}

📋 ವಿಷಯ ನಿರ್ದೇಶನಗಳು:
{depth_instructions}
{style_instructions}
{richness_instructions}

📏 ನಿಖರ ಅವಶ್ಯಕತೆಗಳು:
• ಅವಧಿ: ನಿಖರವಾಗಿ {duration} ನಿಮಿಷಗಳು (ಸುಮಾರು {total_words} ಪದಗಳು)
• ಭಾಷೆ: ಶುದ್ಧ ಕನ್ನಡ, ಸರಳ ಮತ್ತು ಸ್ಪಷ್ಟ
• ರಚನೆ: ಆಕರ್ಷಕ ಪರಿಚಯ → ಮುಖ್ಯ ವಿಷಯ → ಪ್ರಭಾವಶಾಲಿ ಮುಕ್ತಾಯ

⚠️ ಮುಖ್ಯ: ಟೆಂಪ್ಲೇಟ್ ಅಥವಾ ಸೂಚನೆಗಳನ್ನು ಬರೆಯಬೇಡಿ. ಪೂರ್ಣ ಸ್ಕ್ರಿಪ್ಟ್ ಮಾತ್ರ ಬರೆಯಿರಿ.

ಈಗ ಯೂಸರ್ ಆಯ್ಕೆಗಳ ಪ್ರಕಾರ ಸಂಪೂರ್ಣ {duration}-ನಿಮಿಷದ ಸೆಗ್ಮೆಂಟ್ ಬರೆಯಿರಿ:
"""