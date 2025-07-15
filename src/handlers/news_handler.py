"""
News script generation handler
"""
import os
from telegram import Update
from telegram.ext import ContextTypes
from src.services.ai_service import AIService
from src.services.category_detector import CategoryDetector
from src.utils.file_manager import FileManager
from src.utils.logger import get_logger

logger = get_logger(__name__)

class NewsHandler:
    def __init__(self):
        self.ai_service = AIService()
        self.category_detector = CategoryDetector()
        self.file_manager = FileManager()
        self.logger = logger
    
    async def handle_news_content(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle news content input and generate scripts"""
        content_text = update.message.text.strip()

        if content_text.lower() in ["❌ stop", "stop", "cancel", "🔴 abort & reset"]:
            await update.message.reply_text("ಪ್ರಕ್ರಿಯೆ ರದ್ದುಪಡಿಸಲಾಗಿದೆ.")
            from src.handlers.start_handler import StartHandler
            start_handler = StartHandler()
            return await start_handler.show_main_menu(update)

        try:
            await update.message.reply_chat_action(action="typing")
            
            # Detect category
            category = self.category_detector.detect_category("", content_text)
            
            # Generate prompts
            av_prompt = self.ai_service.generate_av_prompt(category, content_text)
            pkg_prompt = self.ai_service.generate_pkg_prompt(category, content_text)
            
            # Generate content
            av_content = self.ai_service.generate_content(av_prompt)
            pkg_content = self.ai_service.generate_content(pkg_prompt)

            # Create output file
            filename = f"news_output_{update.message.chat.id}.txt"
            file_path = self.file_manager.assemble_output_file(
                "News Script", category, av_content, pkg_content, filename
            )

            # Send response
            await update.message.reply_text(f"✅ Category: {category}\nಫೈಲ್ ಕಳುಹಿಸಲಾಗುತ್ತಿದೆ...")
            
            with open(file_path, 'rb') as file:
                await context.bot.send_document(
                    chat_id=update.message.chat_id,
                    document=file,
                    filename=filename,
                    caption="📝 ನಿಮ್ಮ ನ್ಯೂಸ್ ಸ್ಕ್ರಿಪ್ಟ್"
                )
            
            # Clean up
            os.remove(file_path)
            
        except Exception as e:
            self.logger.error(f"Error in handle_news_content: {e}")
            await update.message.reply_text("ಕ್ಷಮಿಸಿ, ಸ್ಕ್ರಿಪ್ಟ್ ರಚನೆಯಲ್ಲಿ ದೋಷ ಸಂಭವಿಸಿದೆ.")

        # Return to main menu
        from src.handlers.start_handler import StartHandler
        start_handler = StartHandler()
        return await start_handler.show_main_menu(update)