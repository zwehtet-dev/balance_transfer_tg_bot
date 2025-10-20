.PHONY: help install run test clean db-shell backup

help:
	@echo "Balance Transfer Bot v2.0 - Available Commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make run       - Run the bot"
	@echo "  make test      - Run tests"
	@echo "  make db-shell  - Open database shell"
	@echo "  make backup    - Backup database"
	@echo "  make clean     - Clean up generated files"

install:
	pip install -r requirements.txt

run:
	python run.py

test:
	pytest tests/ -v --cov=bot

db-shell:
	sqlite3 data/bot.db

backup:
	@mkdir -p backups
	@cp data/bot.db backups/bot_$$(date +%Y%m%d_%H%M%S).db
	@echo "Database backed up to backups/"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf data/bot.db-journal
