"""
File Management Utilities (migrated from your file_generator.py)
"""
import os
from pathlib import Path
from src.config.settings import settings

class FileManager:
    def __init__(self):
        self.exports_dir = Path(settings.exports_dir)
        self.uploads_dir = Path(settings.uploads_dir)
        
        # Create directories if they don't exist
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
    
    def assemble_output_file(self, input_type: str, category: str, av_content: str, pkg_content: str, filename: str) -> str:
        """
        Assembles the final AV & PKG content into a single .txt file.
        Returns the file path.
        """
        content = f"""Input Type: {input_type}
Category: {category}

--- SPEED 50 ---
{av_content}

--- PKG SCRIPT ---
{pkg_content}
"""
        
        file_path = self.exports_dir / filename
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        return str(file_path)

    def generate_segment_txt(self, topic, content_type, info_source, detail_level, presentation_style, content_richness, duration):
        """
        Generates a text file for a custom segment with the provided details.
        """
        content = (
            f"ವಿಷಯ: {topic}\n"
            f"ಪ್ರಕಾರ: {content_type}\n"
            f"ಮೂಲ: {info_source}\n"
            f"ವಿವರ: {detail_level}\n"
            f"ಶೈಲಿ: {presentation_style}\n"
            f"ಸಮೃದ್ಧಿ: {content_richness}\n"
            f"ಅವಧಿ: {duration} ನಿಮಿಷಗಳು"
        )
        
        # Create filename
        filename = f"segment_{topic.replace(' ', '_')}.txt"
        file_path = self.exports_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
            
        return str(file_path)