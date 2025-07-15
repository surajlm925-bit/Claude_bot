"""
Custom Segment Creation Handler
"""
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from src.services.ai_service import AIService
from src.utils.file_manager import FileManager
from src.config.constants import *
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SegmentHandler:
    def __init__(self):
        self.ai_service = AIService()
        self.file_manager = FileManager()
        self.logger = logger
    
    async def handle_segment_topic(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle segment topic input"""
        topic = update.message.text.strip()
        
        if topic.lower() in ["❌ stop", "stop", "cancel"]:
            await update.message.reply_text("ಸೆಗ್ಮೆಂಟ್ ರಚನೆ ರದ್ದುಪಡಿಸಲಾಗಿದೆ.")
            from src.handlers.start_handler import StartHandler
            start_handler = StartHandler()
            return await start_handler.show_main_menu(update)
        
        if not topic:
            await update.message.reply_text("ದಯವಿಟ್ಟು ಮಾನ್ಯ ವಿಷಯವನ್ನು ನಮೂದಿಸಿ.")
            return SEGMENT_TOPIC
        
        # Store topic
        context.user_data["segment_topic"] = topic
        
        # Start interactive questions
        q1_keyboard = [
            ["📰 ಇತ್ತೀಚಿನ ಸುದ್ದಿ/ಘಟನೆಗಳು"],
            ["📚 ಸಾಮಾನ್ಯ ಜ್ಞಾನ/ಶಿಕ್ಷಣ"],
            ["🎭 ಮನರಂಜನೆ/ಸಂಸ್ಕೃತಿ"],
            ["❌ ರದ್ದುಮಾಡಿ"]
        ]
        reply_markup = ReplyKeyboardMarkup(q1_keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            f"✅ ವಿಷಯ: '{topic}'\n\n"
            "❓ ಪ್ರಶ್ನೆ 1/5: ಈ ವಿಷಯವು ಯಾವ ಪ್ರಕಾರದ್ದು?",
            reply_markup=reply_markup
        )
        return SEGMENT_Q1

        async def handle_segment_q1(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle Question 1: Content Type"""
        choice = update.message.text.strip()
        
        if choice == "❌ ರದ್ದುಮಾಡಿ":
            await update.message.reply_text("ಸೆಗ್ಮೆಂಟ್ ರಚನೆ ರದ್ದುಪಡಿಸಲಾಗಿದೆ.")
            from src.handlers.start_handler import StartHandler
            start_handler = StartHandler()
            return await start_handler.show_main_menu(update)
        
        context.user_data["segment_content_type"] = choice
        
        q2_keyboard = [
            ["🔍 ವೆಬ್ ಸರ್ಚ್ + AI ಜ್ಞಾನ"],
            ["🧠 ಕೇವಲ AI ಜ್ಞಾನ"],
            ["🎯 ನೀವೇ ನಿರ್ಧರಿಸಿ"],
            ["❌ ರದ್ದುಮಾಡಿ"]
        ]
        reply_markup = ReplyKeyboardMarkup(q2_keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            "❓ ಪ್ರಶ್ನೆ 2/5: ಮಾಹಿತಿ ಮೂಲ ಆಯ್ಕೆಮಾಡಿ:",
            reply_markup=reply_markup
        )
        return SEGMENT_Q2

    async def handle_segment_q2(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle Question 2: Information Source"""
        choice = update.message.text.strip()
        
        if choice == "❌ ರದ್ದುಮಾಡಿ":
            await update.message.reply_text("ಸೆಗ್ಮೆಂಟ್ ರಚನೆ ರದ್ದುಪಡಿಸಲಾಗಿದೆ.")
            from src.handlers.start_handler import StartHandler
            start_handler = StartHandler()
            return await start_handler.show_main_menu(update)
        
        context.user_data["segment_info_source"] = choice
        
        q3_keyboard = [
            ["📊 ಸಂಕ್ಷಿಪ್ತ ಮಾಹಿತಿ"],
            ["📋 ಮಧ್ಯಮ ವಿವರಣೆ"],
            ["📖 ವಿಸ್ತೃತ ವಿವರಣೆ"],
            ["🎓 ಸಮಗ್ರ ಸ್ಕ್ರಿಪ್ಟ್"],
            ["❌ ರದ್ದುಮಾಡಿ"]
        ]
        reply_markup = ReplyKeyboardMarkup(q3_keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            "❓ ಪ್ರಶ್ನೆ 3/5: ವಿಷಯದ ವಿವರ ಮಟ್ಟ ಆಯ್ಕೆಮಾಡಿ:",
            reply_markup=reply_markup
        )
        return SEGMENT_Q3

    async def handle_segment_q3(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle Question 3: Detail Level"""
        choice = update.message.text.strip()
        
        if choice == "❌ ರದ್ದುಮಾಡಿ":
            await update.message.reply_text("ಸೆಗ್ಮೆಂಟ್ ರಚನೆ ರದ್ದುಪಡಿಸಲಾಗಿದೆ.")
            from src.handlers.start_handler import StartHandler
            start_handler = StartHandler()
            return await start_handler.show_main_menu(update)
        
        context.user_data["segment_detail_level"] = choice
        
        q4_keyboard = [
            ["📺 ಟಿವಿ ನ್ಯೂಸ್ ಶೈಲಿ"],
            ["🎙️ ರೇಡಿಯೋ ಶೈಲಿ"],
            ["📖 ಶೈಕ್ಷಣಿಕ ಶೈಲಿ"],
            ["💬 ಸಂಭಾಷಣಾ ಶೈಲಿ"],
            ["❌ ರದ್ದುಮಾಡಿ"]
        ]
        reply_markup = ReplyKeyboardMarkup(q4_keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            "❓ ಪ್ರಶ್ನೆ 4/5: ಪ್ರಸ್ತುತಿ ಶೈಲಿ ಆಯ್ಕೆಮಾಡಿ:",
            reply_markup=reply_markup
        )
        return SEGMENT_Q4

    async def handle_segment_q4(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle Question 4: Presentation Style"""
        choice = update.message.text.strip()
        
        if choice == "❌ ರದ್ದುಮಾಡಿ":
            await update.message.reply_text("ಸೆಗ್ಮೆಂಟ್ ರಚನೆ ರದ್ದುಪಡಿಸಲಾಗಿದೆ.")
            from src.handlers.start_handler import StartHandler
            start_handler = StartHandler()
            return await start_handler.show_main_menu(update)
        
        context.user_data["segment_presentation_style"] = choice
        
        q5_keyboard = [
            ["🎯 ಮುಖ್ಯ ವಿಷಯ ಮಾತ್ರ"],
            ["📝 ಉದಾಹರಣೆಗಳೊಂದಿಗೆ"],
            ["🌟 ಕಥೆಗಳು + ಉದಾಹರಣೆಗಳು"],
            ["🎭 ಸಂವಾದಾತ್ಮಕ ವಿಷಯ"],
            ["❌ ರದ್ದುಮಾಡಿ"]
        ]
        reply_markup = ReplyKeyboardMarkup(q5_keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            "❓ ಪ್ರಶ್ನೆ 5/5: ವಿಷಯ ಸಮೃದ್ಧಿ ಆಯ್ಕೆಮಾಡಿ:",
            reply_markup=reply_markup
        )
        return SEGMENT_Q5

    async def handle_segment_q5(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle Question 5: Content Richness - Then Duration Selection"""
        choice = update.message.text.strip()
        
        if choice == "❌ ರದ್ದುಮಾಡಿ":
            await update.message.reply_text("ಸೆಗ್ಮೆಂಟ್ ರಚನೆ ರದ್ದುಪಡಿಸಲಾಗಿದೆ.")
            from src.handlers.start_handler import StartHandler
            start_handler = StartHandler()
            return await start_handler.show_main_menu(update)
        
        context.user_data["segment_content_richness"] = choice
        
        # Show user their selections
        summary = f"""
✅ ನಿಮ್ಮ ಆಯ್ಕೆಗಳು:
━━━━━━━━━━━━━━━━━
📌 ವಿಷಯ: {context.user_data.get('segment_topic', 'N/A')}
🎯 ಪ್ರಕಾರ: {context.user_data.get('segment_content_type', 'N/A')}
🔍 ಮೂಲ: {context.user_data.get('segment_info_source', 'N/A')}
📋 ವಿವರ: {context.user_data.get('segment_detail_level', 'N/A')}
🎙️ ಶೈಲಿ: {context.user_data.get('segment_presentation_style', 'N/A')}
🌟 ಸಮೃದ್ಧಿ: {choice}
"""
        
        await update.message.reply_text(summary)
        
        # Ask for duration
        duration_keyboard = [
            ["2", "3", "5"],
            ["7", "10", "15"],
            ["❌ ರದ್ದುಮಾಡಿ"]
        ]
        reply_markup = ReplyKeyboardMarkup(duration_keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            "⏱️ ಅಂತಿಮ ಪ್ರಶ್ನೆ: ಸೆಗ್ಮೆಂಟ್ ಅವಧಿ ಆಯ್ಕೆಮಾಡಿ (ನಿಮಿಷಗಳಲ್ಲಿ):",
            reply_markup=reply_markup
        )
        return SEGMENT_DURATION

    async def handle_segment_duration(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle segment duration input"""
        duration = update.message.text.strip()
        
        if duration == "❌ ರದ್ದುಮಾಡಿ":
            await update.message.reply_text("ಸೆಗ್ಮೆಂಟ್ ರಚನೆ ರದ್ದುಪಡಿಸಲಾಗಿದೆ.")
            from src.handlers.start_handler import StartHandler
            start_handler = StartHandler()
            return await start_handler.show_main_menu(update)
        
        try:
            # Validate duration is a positive number
            duration_int = int(duration)
            if duration_int <= 0:
                raise ValueError("Duration must be positive")
        except ValueError:
            await update.message.reply_text("⚠️ ದಯವಿಟ್ಟು ಮಾನ್ಯ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ (ಉದಾಹರಣೆ: 2, 5, 10)")
            return SEGMENT_DURATION
        
        context.user_data['segment_duration'] = duration_int
        await update.message.reply_text(
            f"✅ ಅವಧಿ: {duration_int} ನಿಮಿಷಗಳು\n\n"
            "🔄 ನಿಮ್ಮ ಕಸ್ಟಮ್ ಸೆಗ್ಮೆಂಟ್ ಅನ್ನು ರಚಿಸಲಾಗುತ್ತಿದೆ...\n"
            "ದಯವಿಟ್ಟು ಕೆಲವು ಸೆಕೆಂಡುಗಳು ಕಾಯಿರಿ.",
            reply_markup=ReplyKeyboardRemove()
        )
        return SEGMENT_PROCESSING

    async def process_segment(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Process segment with collected parameters and show results"""
        try:
            # Get user preferences
            user_prefs = {
                'topic': context.user_data.get('segment_topic', ''),
                'content_type': context.user_data.get('segment_content_type', ''),
                'info_source': context.user_data.get('segment_info_source', ''),
                'detail_level': context.user_data.get('segment_detail_level', ''),
                'presentation_style': context.user_data.get('segment_presentation_style', ''),
                'content_richness': context.user_data.get('segment_content_richness', ''),
            }
            duration = context.user_data.get('segment_duration', 5)
            
            # Import segment service
            from src.services.segment_service import SegmentService
            segment_service = SegmentService()
            
            # Generate segment
            segment_text, category, sources = await segment_service.generate_custom_segment(
                user_prefs, duration
            )
            
            # Generate the text file
            file_path = self.file_manager.generate_segment_txt(
                topic=user_prefs['topic'],
                content_type=user_prefs['content_type'],
                info_source=user_prefs['info_source'],
                detail_level=user_prefs['detail_level'],
                presentation_style=user_prefs['presentation_style'],
                content_richness=user_prefs['content_richness'],
                duration=duration
            )

            # Send success message
                        # Send success message
            await update.message.reply_text(
                f"✅ ಸೆಗ್ಮೆಂಟ್ ಯಶಸ್ವಿಯಾಗಿ ರಚಿಸಲಾಗಿದೆ!\n\n"
                f"📊 ವಿವರಗಳು:\n"
                f"• ವಿಷಯ: {user_prefs['topic']}\n"
                f"• ಅವಧಿ: {duration} ನಿಮಿಷಗಳು\n"
                f"• ವರ್ಗ: {category}\n"
                f"• ಮೂಲಗಳು: {sources}"
            )

            # Send the file
            with open(file_path, 'rb') as file:
                await update.message.reply_document(
                    document=file, 
                    caption="🎬 ನಿಮ್ಮ ಕಸ್ಟಮ್ ಸೆಗ್ಮೆಂಟ್ ಫೈಲ್ ಸಿದ್ಧವಾಗಿದೆ!"
                )
            
            # Cleanup
            import os
            os.remove(file_path)
            
        except KeyError as e:
            self.logger.error(f"KeyError in process_segment: {e}")
            await update.message.reply_text(f"⚠️ ಸೆಗ್ಮೆಂಟ್ ಪ್ರಕ್ರಿಯೆ ವಿಫಲವಾಗಿದೆ: {e}")
        except Exception as e:
            self.logger.error(f"Segment processing failed: {str(e)}", exc_info=True)
            await update.message.reply_text("⚠️ ಸೆಗ್ಮೆಂಟ್ ಪ್ರಕ್ರಿಯೆ ವಿಫಲವಾಗಿದೆ")
        
        # Clear context and return to main menu
        context.user_data.clear()
        from src.handlers.start_handler import StartHandler
        start_handler = StartHandler()
        return await start_handler.show_main_menu(update)