"""
AI Content Generation Service (complete version)
"""
import google.generativeai as genai
import logging
from typing import Optional
from src.config.settings import settings

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.model = self._configure_gemini()
    
    def _configure_gemini(self):
        """Configure Gemini AI model"""
        genai.configure(api_key=settings.gemini_api_key)
        return genai.GenerativeModel('models/gemini-1.5-flash')
    
    def generate_av_prompt(self, category: str, content_text: str) -> str:
        """Generate AV prompt (from your original code)"""
        return f"""
        {category} ವಿಭಾಗಕ್ಕೆ ಸಂಬಂಧಿಸಿದಂತೆ, ಕೆಳಗಿನ ಮಾಹಿತಿಯನ್ನು ಆಧರಿಸಿ ಒಂದು ಶಕ್ತಿಯುತವಾದ, ಶುದ್ಧ ಕನ್ನಡದಲ್ಲಿ ಬರೆಯಲ್ಪಟ್ಟ ಎಐ ಆಧಾರಿತ ಶೀರ್ಷಿಕೆ ರೂಪಿಸಿ. 

        ಇದರ ಆವೃತ್ತಿ ಟಿವಿ ನ್ಯೂಸ್ ಎಂಕರ್ ಉಚ್ಚಾರಣೆಗೆ ಅನುಗುಣವಾಗಿ, ಒಂದು ಹೂರಣದಂತೆ ಇರಲಿ. ಅಂದರೆ, ಬೇರೆ ಬೇರೆ ವಾಕ್ಯಗಳ ಬದಲು ನಿರಂತರವಾಗಿ ಓದಬಹುದಾದ, ತೀವ್ರ ಶೈಲಿಯ ಒಂದು ಪ್ಯಾರಾಗ್ರಾಫ್ ಆಗಿರಬೇಕು.

        ವಿಷಯ:
        {content_text}

        ಇದನ್ನು ಒಂದು ಶಕ್ತಿಯುತ ಕನ್ನಡ ಪ್ಯಾರಾಗ್ರಾಫ್ ರೂಪದಲ್ಲಿ ಬರೆಯಿರಿ.
        """
    
    def generate_pkg_prompt(self, category: str, content_text: str) -> str:
        """Generate PKG prompt (from your original code)"""
        return f"""
ನೀವು ಕನ್ನಡದ ಹಿರಿಯ ಸುದ್ದಿ ವರದಿಗಾರರಾಗಿದ್ದು, ಈ ಸುದ್ದಿ '{category}' ವರ್ಗಕ್ಕೆ ಸೇರಿದ ವರದಿ. ಕೆಳಗಿನ ಮಾಹಿತಿಯ ಆಧಾರದ ಮೇಲೆ ಸಂಪೂರ್ಣ ಪ್ಯಾಕೇಜ್ ಸ್ಕ್ರಿಪ್ಟ್ (PKG Script) ಸಿದ್ಧಪಡಿಸಿ.

ಸ್ಕ್ರಿಪ್ಟ್ ಫಾರ್ಮಾಟ್ ಈ ರೀತಿ ಇರಲಿ:

📦 ಪ್ಯಾಕೇಜ್ ಸ್ಕ್ರಿಪ್ಟ್ (PKG Script)

Headline:
"<ಮುಖ್ಯ ಶೀರ್ಷಿಕೆ>"

Script:

🎙 ಆಂಕರ್ ಇಂಟ್ರೋ:
<ಗಮನ ಸೆಳೆಯುವ ಆರಂಭ, ವಿಷಯ ಪರಿಚಯ, ಸುದ್ದಿ ಸದ್ಯ ಎಷ್ಟು ಮಹತ್ವದ್ದಾಗಿದೆ ಎಂಬ ಬಿಂಬ>

🎙 ಹಿನ್ನೆಲೆ:
<ಈ ವಿಷಯದ ಹಿಂದಿನ ಹಿನ್ನೆಲೆ, ಈ ಹಿಂದೆ ಏನು ನಡೆದಿದೆ, ಸಂಬಂಧಿತ ಘಟನೆಗಳು>

🎙 ವರದಿ:
<ಪೂರ್ಣ ವಿಷಯ ವಿವರಣೆ, ಘಟನೆಯ ವಿಷಯಗಳು, ತೀವ್ರತೆ, ಸ್ಥಳೀಯರ ಪ್ರತಿಕ್ರಿಯೆ>

🎙 ಮುಕ್ತಾಯ:
<ಅಧಿಕಾರಿಗಳ ಸ್ಪಂದನೆ ಸಾಧ್ಯತೆ, ಮುಂದಿನ ನಡೆಯ ಬಗ್ಗೆ ಪ್ರಶ್ನಾತ್ಮಕ ಮುಕ್ತಾಯ>

ವಿಷಯ:
{content_text}
        """

    def generate_speed50_av_prompt(self, content_text: str, category: str = "ಸಾಮಾನ್ಯ") -> str:
        """Generate Speed 50 AV prompt"""
        return f"""
ನೀವು ಕನ್ನಡ ವಾರ್ತಾ ಆಂಕರ್. ಈ ಕೆಳಗಿನ '{category}' ವಿಷಯಕ್ಕಾಗಿ 60-90 ಸೆಕೆಂಡುಗಳ AV ಸ್ಕ್ರಿಪ್ಟ್ ರಚಿಸಿ:

ನಿಯಮಗಳು:
1. 1 ಪ್ಯಾರಾಗ್ರಾಫ್ ಮಾತ್ರ (4-5 ವಾಕ್ಯಗಳು)
2. ಪ್ರತಿ ಶೀರ್ಷಿಕೆಗೆ ಸ್ವತಂತ್ರ ಸ್ಕ್ರಿಪ್ಟ್
3. ಸ್ಥಳ, ಘಟನೆ, ಪ್ರಮುಖ ವಿವರಗಳು, ಒಂದು ಉಲ್ಲೇಖಿತ ಹೇಳಿಕೆ ಸೇರಿಸಿ
4. ಶುದ್ಧ ಕನ್ನಡ, ಯಾವುದೇ ಇಂಗ್ಲಿಷ್ ಪದಗಳಿಲ್ಲ
5. TV ಶೈಲಿಯಲ್ಲಿ ಸರಳ ಮತ್ತು ಸ್ಪಷ್ಟವಾಗಿ

ವಿಷಯ:
{content_text}
"""
    
    def generate_content(self, prompt: str) -> str:
        """Generate content using Gemini"""
        try:
            response = self.model.generate_content(
                prompt,
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
            )
            return response.text.strip() if response.text else "ಸಂಪಾದನೆ ಸಾಧ್ಯವಾಗಿಲ್ಲ."
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            if "quota" in str(e).lower():
                return "ಕ್ಷಮಿಸಿ, API ಮಿತಿ ತಲುಪಿದೆ. ದಯವಿಟ್ಟು ನಂತರ ಪ್ರಯತ್ನಿಸಿ."
            elif "invalid" in str(e).lower():
                return "ದೋಷ: ಅಮಾನ್ಯ ವಿನಂತಿ. ದಯವಿಟ್ಟು ನಿಮ್ಮ ಇನ್ಪುಟ್ ಪರಿಶೀಲಿಸಿ."
            else:
                return "ಕ್ಷಮಿಸಿ, ಸೇವೆಯಲ್ಲಿ ತಾತ್ಕಾಲಿಕ ತೊಂದರೆ. ದಯವಿಟ್ಟು ನಂತರ ಪ್ರಯತ್ನಿಸಿ."