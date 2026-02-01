# Installation Guide - EliteTestBot Checker

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Getting Telegram Credentials](#getting-telegram-credentials)
3. [Installation Steps](#installation-steps)
4. [Configuration](#configuration)
5. [First Run](#first-run)
6. [Troubleshooting](#troubleshooting)

## System Requirements

- **Python**: 3.10 or higher
- **Operating System**: Windows, Linux, or macOS
- **RAM**: Minimum 512MB
- **Storage**: 100MB free space
- **Network**: Stable internet connection

## Getting Telegram Credentials

### 1. Get API ID and API Hash

1. Visit [https://my.telegram.org](https://my.telegram.org)
2. Log in with your phone number
3. Go to "API Development Tools"
4. Create a new application:
   - App title: `EliteTestBot Checker`
   - Short name: `mat1520`
   - Platform: Choose appropriate platform
5. Copy your `api_id` and `api_hash`

### 2. Get Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions:
   - Choose a name: `EliteTestBot Checker`
   - Choose a username: `EliteTestBot` (must end with 'bot')
4. Copy the bot token provided

### 3. Create Log Channel (Optional)

1. Create a private channel in Telegram
2. Add your bot as administrator
3. Send a message in the channel
4. Forward the message to [@username_to_id_bot](https://t.me/username_to_id_bot)
5. Copy the channel ID (it will be negative, like `-1003870179755`)

## Installation Steps

### Windows

1. **Download and Install Python**
   - Visit [python.org](https://www.python.org/downloads/)
   - Download Python 3.10+
   - **Important**: Check "Add Python to PATH" during installation

2. **Clone or Download the Project**
   ```bash
   # Using Git
   git clone https://github.com/SkyBotsDeveloper/telegram-card-checker-bot.git
   cd telegram-card-checker-bot

   # Or download ZIP and extract
   ```

3. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   ```

4. **Activate Virtual Environment**
   ```bash
   .venv\Scripts\activate
   ```

5. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Linux/macOS

1. **Install Python** (if not already installed)
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3.10 python3.10-venv python3-pip

   # macOS (using Homebrew)
   brew install python@3.10
   ```

2. **Clone the Project**
   ```bash
   git clone https://github.com/SkyBotsDeveloper/telegram-card-checker-bot.git
   cd telegram-card-checker-bot
   ```

3. **Create Virtual Environment**
   ```bash
   python3 -m venv .venv
   ```

4. **Activate Virtual Environment**
   ```bash
   source .venv/bin/activate
   ```

5. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Method 1: Environment Variables (Recommended)

1. **Copy the example file**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file**
   ```env
   TELEGRAM_API_ID=12345678
   TELEGRAM_API_HASH=1234567890abcdef1234567890abcdef
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_CHANNEL_LOGS=-1003870179755
   ```

### Method 2: Direct Configuration

Edit `main.py` and replace the placeholder values:

```python
API_ID = '12345678'  # Your API ID
API_HASH = '1234567890abcdef1234567890abcdef'  # Your API Hash
BOT_TOKEN = '1234567890:ABCdefGHIjklMNOpqrsTUVwxyz'  # Your Bot Token
CHANNEL_LOGS = '-1003870179755'  # Your Channel ID (optional)
```

## First Run

1. **Activate Virtual Environment** (if not already active)
   ```bash
   # Windows
   .venv\Scripts\activate

   # Linux/macOS
   source .venv/bin/activate
   ```

2. **Run the Bot**
   ```bash
   python main.py
   ```

3. **Verify Bot is Running**
   You should see output like:
   ```
   INFO:pyrogram.client:Pyrogram v2.0.106 (layer 158)
   INFO:root:Bot started successfully
   ```

4. **Test the Bot**
   - Open Telegram
   - Search for your bot
   - Send `/start` command
   - You should receive a welcome message

## Troubleshooting

### Common Issues

#### 1. "Python is not recognized"
**Solution**: Add Python to PATH
- Windows: Reinstall Python and check "Add to PATH"
- Linux/macOS: Use full path `/usr/bin/python3`

#### 2. "No module named 'pyrogram'"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

#### 3. "Invalid API_ID or API_HASH"
**Solution**: 
- Verify credentials from my.telegram.org
- Ensure no extra spaces in configuration
- API_ID should be a number
- API_HASH should be 32 characters

#### 4. "Bot token invalid"
**Solution**:
- Get new token from @BotFather
- Token format: `NUMBER:LETTERS` (e.g., `123456:ABC-DEF`)

#### 5. Database errors
**Solution**:
```bash
# Delete existing database (will lose data)
rm db_bot.db bins.db

# Or on Windows
del db_bot.db bins.db

# Restart bot
python main.py
```

#### 6. Port already in use
**Solution**:
- Check if bot is already running
- Kill existing process
- Restart bot

### Getting Help

1. **Check Logs**
   - Look at console output
   - Check for error messages

2. **Verify Configuration**
   ```bash
   # Test Python version
   python --version

   # Test dependencies
   pip list | grep -i pyrogram
   ```

3. **Common Commands**
   ```bash
   # Update dependencies
   pip install -r requirements.txt --upgrade

   # Clear Python cache
   find . -type d -name __pycache__ -exec rm -r {} +

   # Deactivate virtual environment
   deactivate
   ```

## Making Bot Admin

To use admin commands:

1. Get your Telegram user ID:
   - Send `/id` to your bot
   - Or use [@userinfobot](https://t.me/userinfobot)

2. Add yourself as admin in the database:
   ```python
   # Run Python in the project directory
   python
   
   >>> from utilsdf.db import Database
   >>> db = Database()
   >>> db.add_premium_membership(YOUR_USER_ID, days=365, credits=10000, rank="Admin")
   >>> exit()
   ```

3. Restart the bot

## Keeping Bot Running 24/7

### Linux (using screen)
```bash
screen -S mat1520
source .venv/bin/activate
python main.py

# Detach: Ctrl+A, then D
# Reattach: screen -r mat1520
```

### Using systemd (Linux)
Create `/etc/systemd/system/mat1520.service`:
```ini
[Unit]
Description=EliteTestBot Checker Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/mat1520-checker
Environment=PATH=/path/to/mat1520-checker/.venv/bin
ExecStart=/path/to/mat1520-checker/.venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable mat1520
sudo systemctl start mat1520
sudo systemctl status mat1520
```

### Windows (using NSSM)
1. Download NSSM from [nssm.cc](https://nssm.cc)
2. Run: `nssm install mat1520`
3. Configure paths to Python and main.py
4. Set startup type to Automatic

## Next Steps

1. Read the [README.md](README.md) for available commands
2. Configure gates in `assets/gates.json`
3. Customize responses in `assets/responses.json`
4. Add premium keys using `/key` command
5. Test gates with sample cards

---

**Need more help?** Check the [main README](README.md) or open an issue on GitHub.
