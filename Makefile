.PHONY: help install install-dev test test-cov lint format type-check run clean setup

# Default target
help:
	@echo "Available commands:"
	@echo "  setup       - Complete setup for local development"
	@echo "  install     - Install production dependencies"
	@echo "  install-dev - Install development dependencies"
	@echo "  test        - Run all tests"
	@echo "  test-cov    - Run tests with coverage"
	@echo "  lint        - Run linting"
	@echo "  format      - Format code with black"
	@echo "  type-check  - Run type checking"
	@echo "  run         - Start development bot"
	@echo "  clean       - Clean temporary files"

# Complete setup
setup: install-dev create-dirs copy-env
	@echo "✅ Setup complete! Don't forget to:"
	@echo "   1. Copy .env.example to .env"
	@echo "   2. Add your TELEGRAM_TOKEN and GEMINI_API_KEY"
	@echo "   3. Run 'make run' to start the bot"

# Create necessary directories
create-dirs:
	@mkdir -p data/{uploads,exports,templates}
	@mkdir -p logs
	@echo "📁 Created data directories"

# Copy environment file
copy-env:
	@if [ ! -f .env ]; then cp .env.example .env; echo "📄 Created .env file"; fi

# Install dependencies
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install pytest pytest-asyncio pytest-cov black flake8 mypy

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

# Code quality
lint:
	flake8 src/ tests/ --max-line-length=100

format:
	black src/ tests/ --line-length=100

type-check:
	mypy src/

# Run bot
run:
	python -m src.main

# Clean temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf data/bot.db
	@echo "🧹 Cleaned temporary files"