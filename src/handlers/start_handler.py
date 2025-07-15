"""
Start command and menu handling
"""
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from src.config.constants import *
from src.utils.logger import get_logger

logger = get_logger(__name__)

class StartHandler:
    def __init__(self):
        self.logger = logger
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle /start command"""
        context.user_data.clear()
        return await self.show_main_menu(update)
    
    async def show_main_menu(self, update: Update) -> int:
        """Show enhanced main menu with better options"""
        keyboard = [
            [MENU_NEWS],
            [MENU_SPEED50],
            [MENU_SEGMENT],
            [MENU_STOP]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "ನಮಸ್ಕಾರ! ದಯವಿಟ್ಟು ನಿಮ್ಮ ಆಯ್ಕೆಮಾಡಿ:\n\n"
            "1. ಸುದ್ದಿ ಸ್ಕ್ರಿಪ್ಟ್ ರಚನೆ\n"
            "2. ಸ್ಪೀಡ್ 50 ತ್ವರಿತ ಸುದ್ದಿ\n"
            "3. ಕಸ್ಟಮ್ ವಿಷಯ ಸೆಗ್ಮೆಂಟ್\n"
            "4. ಬಾಟ್ ನಿಲ್ಲಿಸಿ",
            reply_markup=reply_markup
        )
        return START
    
    def normalize_input(self, text: str) -> str:
        """Normalize menu input by removing extra spaces and case sensitivity"""
        return text.strip().lower()
    
    async def menu_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle menu choices with better input processing"""
        user_input = self.normalize_input(update.message.text)
        self.logger.info(f"Menu choice received: {user_input}")

        try:
            # Match against normalized versions of menu options
            if user_input == self.normalize_input(MENU_NEWS):
                await update.message.reply_text(
                    "📝 ಸುದ್ದಿ ಸ್ಕ್ರಿಪ್ಟ್ ಮೋಡ್ ಆಯ್ಕೆಮಾಡಲಾಗಿದೆ\n"
                    "ದಯವಿಟ್ಟು ಸುದ್ದಿಯ ಪಠ್ಯವನ್ನು ನಮೂದಿಸಿ:",
                    reply_markup=ReplyKeyboardRemove()
                )
                return NEWS_CONTENT

            elif user_input == self.normalize_input(MENU_SPEED50):
                await update.message.reply_text(
                    "⚡ Speed 50 ಮೋಡ್ ಆಯ್ಕೆಮಾಡಲಾಗಿದೆ\n"
                    "ಪಠ್ಯ ಪೇಸ್ಟ್ ಅಥವಾ ಡಾಕ್ಯುಮೆಂಟ್ ಅಪ್ಲೋಡ್ ಆಯ್ಕೆಮಾಡಿ:",
                    reply_markup=ReplyKeyboardMarkup([
                        ["📋 Paste Headlines", "📄 Upload Word Document"],
                        ["🔴 Abort & Reset"]
                    ], one_time_keyboard=True, resize_keyboard=True)
                )
                return SPEED_50

            elif user_input == self.normalize_input(MENU_SEGMENT):
                await update.message.reply_text(
                    "🎬 ಕಸ್ಟಮ್ ಸೆಗ್ಮೆಂಟ್ ಮೋಡ್ ಆಯ್ಕೆಮಾಡಲಾಗಿದೆ\n"
                    "ದಯವಿಟ್ಟು ಸೆಗ್ಮೆಂಟ್ ವಿಷಯವನ್ನು ನಮೂದಿಸಿ:",
                    reply_markup=ReplyKeyboardRemove()
                )
                return SEGMENT_TOPIC

            elif user_input in [self.normalize_input(MENU_STOP), self.normalize_input("🔴 Abort & Reset")]:
                await update.message.reply_text(
                    "❌ ಕಾರ್ಯಾಚರಣೆ ರದ್ದುಗೊಳಿಸಲಾಗಿದೆ\n"
                    "ಮುಖ್ಯ ಮೆನುಗೆ ಮರಳಲು /start ಒತ್ತಿರಿ",
                    reply_markup=ReplyKeyboardRemove()
                )
                from telegram.ext import ConversationHandler
                return ConversationHandler.END

            else:
                await update.message.reply_text(
                    "⚠️ ತಪ್ಪಾದ ಆಯ್ಕೆ! ದಯವಿಟ್ಟು ಕೆಳಗಿನ ಮೆನು ಆಯ್ಕೆಗಳಲ್ಲಿ ಒಂದನ್ನು ಆರಿಸಿ:",
                    reply_markup=ReplyKeyboardRemove()
                )
                return await self.show_main_menu(update)

        except Exception as e:
            self.logger.error(f"Menu handling error: {str(e)}", exc_info=True)
            await update.message.reply_text(
                "⚠️ ತಾಂತ್ರಿಕ ಸಮಸ್ಯೆ ಸಂಭವಿಸಿದೆ. ದಯವಿಟ್ಟು ಕೆಲವು ನಿಮಿಷಗಳ ನಂತರ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
                reply_markup=ReplyKeyboardRemove()
            )
            from telegram.ext import ConversationHandler
            return ConversationHandler.END