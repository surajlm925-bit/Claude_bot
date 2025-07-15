"""
Main bot orchestration with improved error handling and monitoring
"""
import asyncio
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from telegram import Update

from src.config.settings import settings
from src.config.constants import *
from src.utils.logger import setup_logging, get_logger
from src.handlers.start_handler import StartHandler
from src.handlers.news_handler import NewsHandler
from src.handlers.speed50_handler import Speed50Handler
from src.handlers.segment_handler import SegmentHandler

class ClaudeNewsBot:
    def __init__(self):
        self.settings = settings
        self.logger = get_logger(__name__)
        self.app = None
        
        # Initialize handlers
        self.start_handler = StartHandler()
        self.news_handler = NewsHandler()
        self.speed50_handler = Speed50Handler()
        self.segment_handler = SegmentHandler()
        
    async def initialize(self):
        """Initialize bot with all handlers and middleware"""
        try:
            # Setup logging
            setup_logging()
            self.logger.info("Initializing Claude News Bot...")
            
            # Create application
            self.app = Application.builder().token(self.settings.telegram_token).build()
            
            # Setup conversation handler
            conv_handler = ConversationHandler(
                entry_points=[CommandHandler("start", self.start_handler.start)],
                states={
                    START: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.start_handler.menu_choice)],
                    NEWS_CONTENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.news_handler.handle_news_content)],
                    SPEED_50: [
                        MessageHandler(filters.TEXT & ~filters.COMMAND, self.speed50_handler.handle_speed50),
                        MessageHandler(filters.Document.ALL, self.speed50_handler.handle_speed50_doc_upload)
                    ],
                    SPEED_50_HEADLINES: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.speed50_handler.handle_speed50_headlines)],
                    SPEED_50_DOC_UPLOAD: [MessageHandler(filters.Document.ALL, self.speed50_handler.handle_speed50_doc_upload)],
                    SEGMENT_TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.segment_handler.handle_segment_topic)],
                    SEGMENT_Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.segment_handler.handle_segment_q1)],
                    SEGMENT_Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.segment_handler.handle_segment_q2)],
                    SEGMENT_Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.segment_handler.handle_segment_q3)],
                    SEGMENT_Q4: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.segment_handler.handle_segment_q4)],
                    SEGMENT_Q5: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.segment_handler.handle_segment_q5)],
                    SEGMENT_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.segment_handler.handle_segment_duration)],
                    SEGMENT_PROCESSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.segment_handler.process_segment)]
                },
                fallbacks=[CommandHandler("start", self.start_handler.start)]
            )
            
            # Add handlers
            self.app.add_handler(conv_handler)
            
            self.logger.info("Bot initialized successfully!")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize bot: {e}")
            raise
        
    async def start(self):
        """Start bot with graceful shutdown handling"""
        try:
            self.logger.info("Starting Claude News Bot...")
            await self.app.run_polling(allowed_updates=Update.ALL_TYPES)
        except KeyboardInterrupt:
            self.logger.info("Bot stopped by user")
        except Exception as e:
            self.logger.error(f"Bot error: {e}")
            raise
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """Graceful shutdown"""
        self.logger.info("Shutting down bot...")
        if self.app:
            await self.app.shutdown()