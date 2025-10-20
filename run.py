#!/usr/bin/env python3
"""
Convenience script to run the bot
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from bot.main import main

if __name__ == '__main__':
    main()
