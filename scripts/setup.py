#!/usr/bin/env python3
"""
Setup script for local development
"""
import os
import sys
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    dirs = [
        "data/uploads",
        "data/exports", 
        "data/templates",
        "data/samples",
        "logs"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {dir_path}")

def setup_env_file():
    """Setup environment file"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if not env_file.exists() and env_example.exists():
        env_file.write_text(env_example.read_text())
        print("✅ Created .env file from .env.example")
        print("⚠️  Please edit .env file and add your tokens!")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("❌ .env.example not found!")

def main():
    """Main setup function"""
    print("🚀 Setting up Claude News Bot for local development...")
    
    # Create directories
    create_directories()
    
    # Setup environment
    setup_env_file()
    
    print("\n✅ Setup complete!")
    print("\n📝 Next steps:")
    print("1. Edit .env file and add your API keys")
    print("2. Run: pip install -r requirements.txt")
    print("3. Run: python -m src.main")

if __name__ == "__main__":
    main()