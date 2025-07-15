"""
Speed 50 (Quick News) Handler
"""
import os
from pathlib import Path
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from docx import Document

from src.services.ai_service import AIService
from src.services.category_detector import CategoryDetector
from src.utils.file_manager import FileManager
from src.config.constants import *
from src.utils.logger import get_logger

logger = get_logger(__name__)

class Speed50Handler:
    def __init__(self):
        self.ai_service = AIService()
        self.category_detector = CategoryDetector()
        self.file_manager = FileManager()
        self.logger = logger
    
    async def handle_speed50(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle Speed 50 option selection"""
        user_choice = update.message.text.strip()

        if user_choice.lower() in ["🔴 abort & reset", "❌ stop", "stop", "cancel"]:
            await update.message.reply_text("Speed 50 ರದ್ದುಪಡಿಸಲಾಗಿದೆ.")
            from src.handlers.start_handler import StartHandler
            start_handler = StartHandler()
            return await start_handler.show_main_menu(update)
        
        if user_choice == "📋 Paste Headlines":
            await update.message.reply_text(
                "ಶೀರ್ಷಿಕೆಗಳನ್ನು ಪೇಸ್ಟ್ ಮಾಡಲು ಮುಂದಾಗಿ. ಪ್ರತಿ ಶೀರ್ಷಿಕೆಯ ನಂತರ '++...++' ಹಾಕಿ.\n\n"
                "ನಿಮ್ಮ ಶೀರ್ಷಿಕೆಗಳನ್ನು ಪೇಸ್ಟ್ ಮಾಡಿದ ನಂತರ, 'Done' ಅಥವಾ 'Cancel' ಟೈಪ್ ಮಾಡಿ.",
                reply_markup=ReplyKeyboardRemove()
            )
            context.user_data["headlines"] = []
            return SPEED_50_HEADLINES

        elif user_choice == "📄 Upload Word Document":
            await update.message.reply_text(
                "ದಯವಿಟ್ಟು Word ಡಾಕ್ಯುಮೆಂಟ್ ಅಪ್ಲೋಡ್ ಮಾಡಿ (.docx ಅಥವಾ .txt ಮಾತ್ರ).",
                reply_markup=ReplyKeyboardRemove()
            )
            return SPEED_50_DOC_UPLOAD
        
        # Invalid choice - show options again
        await update.message.reply_text(
            "⚠️ ದಯವಿಟ್ಟು ಮಾನ್ಯ ಆಯ್ಕೆಯನ್ನು ಆರಿಸಿ:",
            reply_markup=ReplyKeyboardMarkup([
                ["📋 Paste Headlines", "📄 Upload Word Document"],
                ["🔴 Abort & Reset"]
            ], one_time_keyboard=True, resize_keyboard=True)
        )
        return SPEED_50

    async def handle_speed50_headlines(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle headlines input for Speed 50"""
        user_input = update.message.text.strip()

        if user_input.lower() in ["cancel", "stop", "❌ stop", "🔴 abort & reset"]:
            await update.message.reply_text("Speed 50 ಪ್ರಕ್ರಿಯೆ ರದ್ದುಪಡಿಸಲಾಗಿದೆ.")
            context.user_data.pop("headlines", None)
            from src.handlers.start_handler import StartHandler
            start_handler = StartHandler()
            return await start_handler.show_main_menu(update)

        if user_input.lower() == "done":
            total = len(context.user_data.get("headlines", []))
            if total == 0:
                await update.message.reply_text("ದಯವಿಟ್ಟು ಕನಿಷ್ಠ 1 ಶೀರ್ಷಿಕೆ ಸೇರಿಸಿ.")
                return SPEED_50_HEADLINES
            else:
                await update.message.reply_text(
                    f"✅ {total} ಶೀರ್ಷಿಕೆ(ಗಳು) ಸ್ವೀಕರಿಸಲಾಗಿದೆ.\n"
                    "ಮುಂದುವರೆಯಲು ದಯವಿಟ್ಟು ಕಾಯಿರಿ..."
                )
                
                # Process headlines
                await self._process_headlines(update, context)
                
                from src.handlers.start_handler import StartHandler
                start_handler = StartHandler()
                return await start_handler.show_main_menu(update)

        # Handle both ++...++ delimited and newline-separated inputs
        headlines = []
        if "++...++" in user_input:
            headlines = [h.strip() for h in user_input.split("++...++") if h.strip()]
        else:
            headlines = [h.strip() for h in user_input.split("\n") if h.strip()]

        if "headlines" not in context.user_data:
            context.user_data["headlines"] = []

        context.user_data["headlines"].extend(headlines)
        await update.message.reply_text(
            f"✅ {len(headlines)} ಶೀರ್ಷಿಕೆ(ಗಳು) ಸೇರಿಸಲಾಗಿದೆ. (ಒಟ್ಟು: {len(context.user_data['headlines'])})\n"
            "ಶೀರ್ಷಿಕೆಗಳನ್ನು ಪೇಸ್ಟ್ ಮಾಡುವುದನ್ನು ಮುಂದುವರಿಸಿ ಅಥವಾ 'Done' ಟೈಪ್ ಮಾಡಿ."
        )
        return SPEED_50_HEADLINES

    async def handle_speed50_doc_upload(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle document upload for Speed 50"""
        try:
            # File validation
            if not update.message.document:
                await update.message.reply_text("⚠️ ದಯವಿಟ್ಟು ಮಾನ್ಯ ಡಾಕ್ಯುಮೆಂಟ್ ಅಪ್ಲೋಡ್ ಮಾಡಿ")
                return SPEED_50
                
            # File type check
            file_ext = os.path.splitext(update.message.document.file_name)[1].lower()
            if file_ext not in ['.txt', '.docx']:
                await update.message.reply_text(f"⚠️ ಅಸಮರ್ಪಕ ಫೈಲ್ ಪ್ರಕಾರ: {file_ext}")
                return SPEED_50

            # Download progress feedback
            await update.message.reply_text(
                f"📥 ಫೈಲ್ '{update.message.document.file_name}' ಡೌನ್ಲೋಡ್ ಆಗುತ್ತಿದೆ..."
            )
            
            # Processing feedback
            await update.message.reply_text(
                f"📄 ಫೈಲ್ ಸ್ವೀಕರಿಸಲಾಗಿದೆ:\n"
                f"ಹೆಸರು: {update.message.document.file_name}\n"
                f"ಗಾತ್ರ: {self._format_size(update.message.document.file_size)}\n"
                "ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಲಾಗುತ್ತಿದೆ..."
            )
            
            # Extract content
            content = await self._extract_content(update, context)
            
            if not content.strip():
                await update.message.reply_text("⚠️ ಡಾಕ್ಯುಮೆಂಟ್ ಖಾಲಿ ಇದೆ")
                return SPEED_50
            
            # Process content as headlines
            headlines = [h.strip() for h in content.split('\n') if h.strip()]
            context.user_data["headlines"] = headlines
            
            await update.message.reply_text(
                f"✅ {len(headlines)} ಹೆಡ್ಲೈನ್ಗಳು ಸ್ವೀಕರಿಸಲ್ಪಟ್ಟಿವೆ\n"
                "ಮುಂದುವರೆಯಲು ದಯವಿಟ್ಟು ಕಾಯಿರಿ..."
            )
            
            # Process headlines
            await self._process_headlines(update, context)
            
            from src.handlers.start_handler import StartHandler
            start_handler = StartHandler()
            return await start_handler.show_main_menu(update)
            
        except Exception as e:
            self.logger.error(f"Document upload failed: {str(e)}")
            await update.message.reply_text("⚠️ ದೋಷ ಸಂಭವಿಸಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ")
            return SPEED_50

    async def _process_headlines(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process headlines and generate Speed 50 content"""
        headlines = context.user_data.get("headlines", [])
        results = ""
        
        for i, headline in enumerate(headlines, start=1):
            try:
                category = self.category_detector.detect_category("", headline)
                prompt = self.ai_service.generate_speed50_av_prompt(headline, category)
                result = self.ai_service.generate_content(prompt)
                results += f"{result}\n\n{'-'*50}\n\n"
            except Exception as e:
                self.logger.error(f"Error generating AV for headline {i}: {e}")
                results += f"⚠️ AV ಸ್ಕ್ರಿಪ್ಟ್ ತಯಾರಿಸಲು ಸಾಧ್ಯವಾಗಿಲ್ಲ.\n\n{'-'*50}\n\n"

        # Save and send file
        filename = f"speed50_output_{update.message.chat.id}.txt"
        file_path = self.file_manager.exports_dir / filename
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(results)

        with open(file_path, "rb") as f:
            await context.bot.send_document(
                chat_id=update.message.chat_id,
                document=f,
                filename=filename,
                caption=f"⚡ Speed 50 ಫಲಿತಾಂಶಗಳು - {len(headlines)} ಶೀರ್ಷಿಕೆಗಳು"
            )

        # Cleanup
        os.remove(file_path)
        context.user_data.pop("headlines", None)

    async def _extract_content(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Extract content from uploaded document"""
        document = update.message.document
        
        # Create temp directory
        temp_dir = Path("data/uploads")
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Download file
        file = await context.bot.get_file(document.file_id)
        file_path = temp_dir / document.file_name
        await file.download_to_drive(file_path)
        
        try:
            file_ext = os.path.splitext(document.file_name)[1].lower()
            
            if file_ext == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif file_ext == '.docx':
                doc = Document(file_path)
                content = "\n".join([para.text for para in doc.paragraphs if para.text])
            else:
                content = ""
                
            return content
            
        finally:
            # Cleanup temp file
            if file_path.exists():
                os.remove(file_path)

    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"