"""
Application constants
"""

# Conversation States
START, NEWS_CONTENT, SPEED_50, SPEED_50_HEADLINES, SPEED_50_DOC_UPLOAD = range(5)
SEGMENT_TOPIC, SEGMENT_Q1, SEGMENT_Q2, SEGMENT_Q3, SEGMENT_Q4, SEGMENT_Q5, SEGMENT_DURATION, SEGMENT_PROCESSING = range(5, 13)

# Menu Constants
MENU_NEWS = "📝 ಸುದ್ದಿ ಸ್ಕ್ರಿಪ್ಟ್ ಪ್ರಾರಂಭಿಸಿ"
MENU_SPEED50 = "⚡ ಸ್ಪೀಡ್ 50 (ತ್ವರಿತ ಸುದ್ದಿ)"
MENU_SEGMENT = "🎬 ಕಸ್ಟಮ್ ಸೆಗ್ಮೆಂಟ್"
MENU_STOP = "❌ ನಿಲ್ಲಿಸಿ"

# Trusted Sources
TRUSTED_SOURCES = [
    "thehindu.com", "indianexpress.com", "hindustantimes.com",
    "timesofindia.indiatimes.com", "ndtv.com", "news18.com",
    "thewire.in", "scroll.in", "deccanherald.com", "telegraphindia.com",
    "livemint.com", "business-standard.com", "pib.gov.in", "prsindia.org",
    "factchecker.in", "altnews.in", "boomlive.in", "thequint.com",
    "indiatoday.in", "publictv.in", "vijaykarnataka.com",
    "kannada.asianetnews.com", "udayavani.com", "republickannada.co.in",
]

# File Extensions
ALLOWED_DOCUMENT_EXTENSIONS = ['.txt', '.docx', '.doc']
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']