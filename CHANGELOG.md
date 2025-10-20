# Changelog

All notable changes to the Balance Transfer Bot.

## [2.1.0] - 2024-10-20

### 🚀 Major Feature - AI Integration

Added AI-powered features using LangChain and Mistral AI!

### Added - AI Features
- ✨ **Natural Language Commands** - Users can send commands in plain English
  - "send 100 to @alice" → Executes transfer
  - "check my balance" → Shows balance
  - "show my transactions" → Shows history
- ✨ **Group Transfer Detection** - Auto-detect transfers in group chats
  - "@alice I sent you $50" → Auto-records transfer
  - Monitors group messages for transfer announcements
- ✨ **AI-Generated Responses** - Natural, conversational responses
- ✨ **LangChain Integration** - Structured output parsing
- ✨ **Mistral AI Support** - Free tier available
- ✨ **OpenAI Support** - Alternative AI provider

### Added - Services
- `bot/services/ai_service.py` - AI service using LangChain
- `bot/handlers/ai_handlers.py` - AI-powered command handlers

### Added - Configuration
- `AI_PROVIDER` - Choose between mistral or openai
- `MISTRAL_API_KEY` - Mistral AI API key
- `AI_MODEL` - AI model to use
- `ENABLE_AI` - Enable/disable AI features
- `MONITOR_GROUPS` - Enable group monitoring
- `AUTO_DETECT_TRANSFERS` - Auto-detect transfers in groups

### Added - Documentation
- `AI_FEATURES.md` - Comprehensive AI features documentation
- `SETUP_AI.md` - Quick setup guide for AI features

### Updated
- `requirements.txt` - Added langchain and langchain-mistralai
- `bot/utils/config.py` - Added AI configuration options
- `bot/services/bot_service.py` - Integrated AI handlers
- `.env.example` - Added AI configuration examples

### Dependencies
- langchain==0.1.0
- langchain-mistralai==0.0.5
- langchain-openai==0.0.5

---

## [2.0.1] - 2024-10-20

### Fixed
- 🐛 Fixed `sqlite3.Row` AttributeError when accessing optional fields
- 🐛 Fixed datetime handling for SQLite timestamp strings
- ✅ Added helper method `_get_row_value()` for safe row access
- ✅ Updated Transaction model to handle both datetime and string timestamps

### Testing
- ✅ All 17 tests passing
- ✅ Verified transfer functionality works correctly

---

## [2.0.0] - 2024-10-20

### 🚀 Major Release - Complete Restructure

This is a complete rewrite with SQLite database and scalable architecture.

### Added - New Architecture
- ✨ SQLite database storage (replaces JSON)
- ✨ Modular architecture with clear separation
- ✨ Service layer pattern (UserService, TransactionService, BalanceService)
- ✨ Repository pattern for data access
- ✨ Database schema with indexes
- ✨ Unlimited transaction history
- ✨ New `/stats` command
- ✨ Enhanced logging to file
- ✨ Comprehensive test suite for v2

### Improved - Architecture
- 🔧 Separated into models/, services/, handlers/, utils/
- 🔧 Database connection management
- 🔧 Better error handling
- 🔧 Performance optimizations with indexes
- 🔧 Scalable design

### Changed - Breaking Changes
- ⚠️ Storage changed from JSON to SQLite
- ⚠️ Package renamed from `balance_bot/` to `bot/`
- ⚠️ Configuration updated for database
- ⚠️ Service interfaces changed

### Removed
- ❌ JSON storage (replaced with SQLite)
- ❌ Old `balance_bot/` structure
- ❌ StorageStrategy abstract class
- ❌ Transaction limit (now unlimited)

### Migration
- See MIGRATION_GUIDE.md for migration from v1.0

---

## [1.0.0] - 2024-10-20 (Deprecated)

### Added - New Features
- ✨ Modular architecture with 8 focused modules
- ✨ Environment-based configuration system
- ✨ Comprehensive unit test suite
- ✨ Automated setup script (`setup.sh`)
- ✨ Convenience runner (`run.py`)
- ✨ Makefile for common commands
- ✨ Transaction history persistence
- ✨ Backup functionality for storage
- ✨ Global error handler for bot
- ✨ File logging in addition to console
- ✨ Result object pattern for operations
- ✨ Factory methods for model creation

### Improved - Enhancements
- 🔧 Separated concerns into layers (presentation, business, data, storage)
- 🔧 Enhanced error handling at all layers
- 🔧 Atomic file writes to prevent corruption
- 🔧 Better input validation
- 🔧 Improved logging with structured format
- 🔧 Type hints throughout codebase
- 🔧 Better encapsulation in models
- 🔧 More user-friendly error messages
- 🔧 Conversation state management
- 🔧 Transaction history limited to configurable size

### Documentation
- 📚 README.md - Comprehensive project documentation
- 📚 QUICKSTART.md - 5-minute setup guide
- 📚 ARCHITECTURE.md - Technical deep dive
- 📚 IMPROVEMENTS.md - List of improvements
- 📚 PROJECT_STRUCTURE.txt - Visual structure
- 📚 CHANGELOG.md - This file
- 📚 Inline code documentation
- 📚 .env.example - Configuration template

### Security
- 🔒 No hardcoded secrets
- 🔒 Environment variable configuration
- 🔒 Input validation at multiple layers
- 🔒 Balance cannot go negative
- 🔒 Atomic file operations
- 🔒 Error messages don't leak sensitive info

### Testing
- ✅ Unit tests for User model
- ✅ Unit tests for Transaction model
- ✅ Unit tests for BalanceService
- ✅ Test fixtures for isolated testing
- ✅ Coverage reporting support

### Developer Experience
- 🛠️ Automated setup script
- 🛠️ Virtual environment support
- 🛠️ Makefile for common tasks
- 🛠️ .gitignore for clean repo
- 🛠️ Clear project structure
- 🛠️ Extensive documentation

### Infrastructure
- 🏗️ Strategy pattern for storage
- 🏗️ Service layer for business logic
- 🏗️ Dependency injection
- 🏗️ Configuration management
- 🏗️ Logging infrastructure
- 🏗️ Error handling framework

---

## Version Comparison

### v1.0.0 (Deprecated)
- JSON file storage
- Limited transaction history (10)
- Single package structure
- File-based operations

### v2.0.0 (Current)
- SQLite database storage
- Unlimited transaction history
- Modular architecture (models, services, handlers, utils)
- SQL-based operations with indexes
- Better performance and scalability
- Enhanced testing
- Production-ready

---

## Future Roadmap

### v2.1.0 (Planned)
- [ ] PostgreSQL storage backend option
- [ ] Multi-user support (>2 users)
- [ ] Transaction categories
- [ ] Export transactions to CSV
- [ ] Scheduled reports

### v2.2.0 (Planned)
- [ ] Web dashboard
- [ ] REST API
- [ ] Webhooks
- [ ] Rate limiting
- [ ] User authentication

### v3.0.0 (Future)
- [ ] Multi-currency support
- [ ] Recurring transfers
- [ ] Budget tracking
- [ ] Analytics dashboard
- [ ] Mobile app integration

---

## Contributing

When contributing, please:
1. Update this CHANGELOG.md
2. Add tests for new features
3. Update documentation
4. Follow existing code style
5. Ensure all tests pass

---

## Links

- Repository: [Your Repo URL]
- Issues: [Your Issues URL]
- Documentation: See README.md
- Quick Start: See QUICKSTART.md
- Architecture: See ARCHITECTURE.md
