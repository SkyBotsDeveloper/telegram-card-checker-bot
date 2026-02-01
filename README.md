# Telegram Card Checker Bot

Professional Telegram bot for credit card BIN validation and payment gateway testing. Built with Python, Pyrogram, and async architecture for high performance and reliability.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Async](https://img.shields.io/badge/Async-HTTPX-orange.svg)

## Features

### Core Functionality
- **BIN Lookup System**: Retrieve detailed credit card BIN information including bank, country, card type, and level
- **Multiple Payment Gateways**: 25+ integrated payment gateway checkers for comprehensive testing
- **Mass Checking**: Batch processing capabilities for testing multiple cards simultaneously
- **Card Generation**: Generate valid card numbers from BIN patterns

### User Management
- **Premium Membership System**: Multi-tier access control with credits and expiration dates
- **User Ranks**: Free, Premium, Seller, and Admin hierarchy with different permissions
- **Key System**: Secure redeemable keys for premium access distribution
- **Credit System**: Track and manage user checking credits

### Administration
- **Admin Panel**: Complete user management, credits allocation, and system configuration
- **User Control**: Ban/unban users, grant/revoke premium access
- **Broadcast System**: Send announcements to all users or specific groups
- **Anti-spam Protection**: Configurable rate limiting and cooldown periods
- **Logs Channel**: Automated logging of important events and transactions

### Technical Features
- **Async Architecture**: Non-blocking I/O operations for optimal performance
- **SQLite Database**: Lightweight local storage for users, keys, and BIN data
- **Multi-language Support**: Configurable response messages
- **Error Handling**: Comprehensive error management and user feedback
- **Session Management**: Persistent Telegram sessions

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- Telegram API credentials from [my.telegram.org](https://my.telegram.org)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/SkyBotsDeveloper/telegram-card-checker-bot.git
cd telegram-card-checker-bot
```

2. **Create a virtual environment**
```bash
python -m venv .venv
```

3. **Activate the virtual environment**

Windows:
```bash
.venv\Scripts\activate
```

Linux/Mac:
```bash
source .venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Configure the bot**

Edit `main.py` and set your credentials:
```python
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
BOT_TOKEN = 'YOUR_BOT_TOKEN'
CHANNEL_LOGS = 'YOUR_LOG_CHANNEL_ID'
```

6. **Run the bot**
```bash
python main.py
```

## 📁 Project Structure

```
EliteTestBot-checker/
├── assets/              # Configuration files and resources
│   ├── banned_bins.json
│   ├── countrys.json
│   ├── gates.json
│   ├── responses.json
│   └── proxies.txt
├── gates/              # Payment gateway checker modules
│   ├── adriana.py
│   ├── aktz.py
│   ├── astharoth.py
│   └── ... (25+ gates)
├── plugins/            # Bot command handlers
│   ├── admin/         # Admin-only commands
│   ├── gates_cmds/    # Gateway command handlers
│   ├── handlers/      # Message handlers
│   └── users/         # User commands
├── utilsdf/           # Utility functions and database
│   ├── db.py          # Database operations
│   ├── functions.py   # Helper functions
│   ├── vars.py        # Constants and variables
│   └── generator.py   # Card generation utilities
├── main.py            # Bot entry point
└── requirements.txt   # Python dependencies
```

## Available Commands

### User Commands
- `/start` - Initialize bot and display welcome message
- `/cmds` - Display all available commands
- `/bin <bin>` - Retrieve BIN information
- `/gbin <bin>` - Generate card numbers from BIN
- `/id` - Display user ID and account status
- `/plan` - Check subscription plan details
- `/key <key>` - Redeem premium access key

### Gateway Commands
Format: `/gatename cc|mm|yyyy|cvv`

Available gateways: adriana, aktz, astharoth, boruto, brenda, darkito, devilsx, djbaby, ghoul, hinata, hoshigaki, ka, ko, lynx, odali, pepe, pussy, rohee, sebas, sexo, zukesito

Example:
```
/adriana 4111111111111111|12|2025|123
```

### Admin Commands
- `/addpremium <user_id> <days> <credits>` - Grant premium membership
- `/removepremium <user_id>` - Revoke premium membership
- `/ban <user_id>` - Ban user from bot
- `/unban <user_id>` - Unban user
- `/broadcast <message>` - Send message to all users
- `/setantispam <seconds>` - Configure rate limiting delay
- `/addgp` - Add group to whitelist
- `/key` - Manage premium access keys

## Configuration

### Database
SQLite databases are automatically created on first run:
- `db_bot.db` - User data, memberships, and keys
- `bins.db` - BIN information cache

### Assets Configuration

#### gates.json
Configure payment gateway settings:
```json
{
  "gate_name": {
    "status": true,
    "response": "Gateway response message",
    "cc": "Required format: xxxx xxxx xxxx xxxx|mm|yyyy|cvv"
  }
}
```

#### responses.json
Customize bot response messages and templates.

#### banned_bins.json
Define blocked BINs to prevent checking.

## Development

### Testing Gateways
Verify gateway functionality with test scripts:

```bash
python test_gates_direct.py
```

Generates detailed test reports for all configured gateways.

### Adding New Gateways

1. Create gateway file in `gates/` directory
2. Implement async function:
```python
async def your_gate(cc: str, month: str, year: str, cvv: str) -> tuple:
    # Gateway testing logic
    return status, message
```

3. Create command handler in `plugins/gates_cmds/`
4. Update `assets/gates.json` configuration

### Code Style
- Follow PEP 8 guidelines
- Use async/await for I/O operations
- Implement proper error handling and logging
- Document complex functions with docstrings

## Premium System Details

### Credit Management
- Each user account maintains a credit balance
- Credits are consumed per gateway check operation
- Admins can allocate credits to users

### Membership Tiers
- **Free**: Limited access to basic features
- **Premium**: Full gateway access with credits
- **Seller**: Advanced features for resellers
- **Admin**: Complete system control

### Key System
- Generate redeemable keys for premium access
- Configure duration and credits per key
- Track key usage and redemption history

## Anti-Spam Configuration

Implement rate limiting to prevent abuse:
```python
/setantispam 5
```
Sets a 5-second cooldown between command executions.

## BIN Lookup Capabilities

Retrieve detailed card information:
- Card brand identification (Visa, Mastercard, American Express, Discover)
- Card type classification (Credit, Debit, Prepaid)
- Card level determination (Classic, Gold, Platinum, Business)
- Issuing bank information
- Country of origin
- Additional BIN metadata

## Security Considerations

- Store sensitive credentials in environment variables
- Never commit tokens or API keys to version control
- Telegram handles user authentication
- Rate limiting prevents system abuse
- Admin operations restricted by user ID verification

## Environment Variables

Configure credentials securely:

```python
import os

API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
```

Create a `.env` file:
```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_BOT_TOKEN=your_bot_token
```

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-gateway`
3. Commit changes: `git commit -m 'Add new payment gateway'`
4. Push to branch: `git push origin feature/new-gateway`
5. Submit a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Legal Disclaimer

This software is provided for educational and testing purposes only. Users are solely responsible for compliance with all applicable laws and regulations. The developers assume no liability for misuse or damages.

**Important:**
- Do not use for unauthorized transactions
- Respect payment gateway terms of service
- Obtain proper authorization before testing
- Comply with local and international laws

## License

Licensed under the MIT License. See [LICENSE](LICENSE) file for complete terms.

## Credits

Built with:
- [Pyrogram](https://github.com/pyrogram/pyrogram) - Telegram MTProto API Client
- [Pyromod](https://github.com/usernein/pyromod) - Pyrogram Extensions
- [HTTPX](https://www.python-httpx.org/) - Async HTTP Client

## Support

Get help:
- Report bugs via GitHub Issues
- Review documentation in `/docs`
- Check existing issues before creating new ones
- Consult [INSTALLATION.md](INSTALLATION.md) for setup help

## Updates

Keep your installation current:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
python main.py
```

---

**Telegram Card Checker Bot** - Professional BIN validation and gateway testing platform
# telegram-card-checker-bot
