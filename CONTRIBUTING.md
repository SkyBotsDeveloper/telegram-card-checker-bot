# Contributing to EliteTestBot Checker

Thank you for considering contributing to EliteTestBot Checker! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Adding New Features](#adding-new-features)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

This project adheres to ethical guidelines. By participating, you agree to:
- Use the tool responsibly and legally
- Respect payment gateway terms of service
- Not use for fraudulent activities
- Maintain user privacy and security

## How Can I Contribute?

### Reporting Bugs
- Use GitHub Issues
- Include Python version, OS, and error messages
- Provide steps to reproduce
- Include relevant logs (remove sensitive data)

### Suggesting Features
- Check if feature already exists
- Describe the use case
- Explain expected behavior
- Consider security implications

### Improving Documentation
- Fix typos and grammar
- Add examples and clarifications
- Update outdated information
- Translate to other languages

### Writing Code
- Fix bugs
- Add new payment gateways
- Improve performance
- Add tests

## Development Setup

### 1. Fork and Clone
```bash
git clone https://github.com/SkyBotsDeveloper/telegram-card-checker-bot.git
cd telegram-card-checker-bot
git remote add upstream https://github.com/SkyBotsDeveloper/telegram-card-checker-bot.git
```

### 2. Create Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 3. Install Development Dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If exists
```

### 4. Configure Pre-commit Hooks (Optional)
```bash
pip install pre-commit
pre-commit install
```

## Coding Standards

### Python Style Guide
- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 88 characters (Black formatter)
- Use meaningful variable names

### Code Examples

**Good:**
```python
async def validate_credit_card(card_number: str, expiry_month: str, 
                               expiry_year: str, cvv: str) -> tuple:
    """
    Validate credit card details.
    
    Args:
        card_number: 16-digit card number
        expiry_month: Two-digit month (01-12)
        expiry_year: Four-digit year
        cvv: Card verification value
        
    Returns:
        Tuple of (status: str, message: str)
    """
    if not card_number or len(card_number) != 16:
        return "Invalid", "Card number must be 16 digits"
    
    # Your logic here
    return status, message
```

**Bad:**
```python
def check(c, m, y, v):
    if not c:
        return "bad"
    # unclear logic
    return x
```

### Async/Await
- Use `async`/`await` for I/O operations
- Avoid blocking operations
- Use `AsyncClient` from httpx

```python
# Good
async with AsyncClient() as client:
    response = await client.get(url)
    
# Bad
response = requests.get(url)  # Blocking
```

### Error Handling
```python
async def payment_gateway(cc: str, month: str, year: str, cvv: str) -> tuple:
    try:
        async with AsyncClient(timeout=30.0) as client:
            response = await client.post(url, data=data)
            
            if response.status_code == 200:
                return "Approved", "Transaction successful"
            else:
                return "Declined", f"HTTP {response.status_code}"
                
    except asyncio.TimeoutError:
        return "Error", "Request timeout"
    except Exception as e:
        return "Error", f"Gateway error: {str(e)}"
```

### Logging
```python
import logging

logger = logging.getLogger(__name__)

async def my_function():
    logger.info("Starting process")
    try:
        # Your code
        logger.debug("Debug information")
    except Exception as e:
        logger.error(f"Error occurred: {e}")
```

## Adding New Features

### Adding a New Payment Gateway

1. **Create Gateway File**
   
   File: `gates/your_gate.py`
   ```python
   from httpx import AsyncClient
   from utilsdf.functions import capture
   
   async def your_gate(cc: str, month: str, year: str, cvv: str) -> tuple:
       """
       Payment gateway checker for YourSite.com
       
       Args:
           cc: Card number
           month: Expiry month (MM)
           year: Expiry year (YYYY)
           cvv: CVV code
           
       Returns:
           tuple: (status, message)
               status: "Approved! ✅" or "Dead! ❌"
               message: Descriptive message
       """
       async with AsyncClient(
           follow_redirects=True,
           verify=False,
           timeout=30.0
       ) as session:
           try:
               # Step 1: Get initial page
               response = await session.get("https://example.com/checkout")
               
               # Step 2: Extract tokens
               token = capture(response.text, 'name="token" value="', '"')
               if not token:
                   return "Dead! ❌", "Error: No token found"
               
               # Step 3: Submit payment
               headers = {
                   "Content-Type": "application/x-www-form-urlencoded",
                   "User-Agent": "Mozilla/5.0..."
               }
               
               data = {
                   "card_number": cc,
                   "exp_month": month,
                   "exp_year": year,
                   "cvv": cvv,
                   "token": token
               }
               
               response = await session.post(
                   "https://example.com/process",
                   headers=headers,
                   data=data
               )
               
               # Step 4: Parse response
               if "success" in response.text.lower():
                   return "Approved! ✅", "Transaction approved"
               elif "insufficient" in response.text.lower():
                   return "Approved! ✅ -» low funds", "Insufficient funds"
               elif "cvv" in response.text.lower():
                   return "Approved! ✅ -» ccn", "CVV mismatch"
               else:
                   msg = capture(response.text, '"error":"', '"')
                   return "Dead! ❌", msg or "Declined"
                   
           except Exception as e:
               return "Dead! ❌", f"Error: {str(e)}"
   ```

2. **Create Command Handler**
   
   File: `plugins/gates_cmds/your_gate.py`
   ```python
   from pyrogram import Client, filters
   from pyrogram.types import Message
   from gates.your_gate import your_gate
   from utilsdf.functions import check_user_access, parse_card
   from utilsdf.cmds_desing import send_gate_response
   
   @Client.on_message(filters.command("yourgate", prefixes=[".", "/"]))
   async def cmd_your_gate(client: Client, m: Message):
       # Check user permissions
       if not await check_user_access(m.from_user.id):
           await m.reply("❌ No tienes acceso a este comando")
           return
       
       # Parse card details
       card_data = parse_card(m.text)
       if not card_data:
           await m.reply("❌ Formato inválido. Usa: /yourgate cc|mm|yyyy|cvv")
           return
       
       cc, month, year, cvv = card_data
       
       # Send processing message
       msg = await m.reply("⏳ Procesando...")
       
       # Execute gate
       status, message = await your_gate(cc, month, year, cvv)
       
       # Send response
       await send_gate_response(
           m, msg, status, message,
           cc, month, year, cvv,
           gate_name="YourGate"
       )
   ```

3. **Update Configuration**
   
   Add to `assets/gates.json`:
   ```json
   {
     "yourgate": {
       "status": true,
       "response": "Your Site Gateway",
       "cc": "Required: xxxx xxxx xxxx xxxx|mm|yyyy|cvv"
     }
   }
   ```

4. **Test Your Gate**
   ```bash
   python
   >>> from gates.your_gate import your_gate
   >>> import asyncio
   >>> result = asyncio.run(your_gate("4111111111111111", "12", "2025", "123"))
   >>> print(result)
   ```

### Adding Admin Commands

File: `plugins/admin/your_command.py`
```python
from pyrogram import Client, filters
from pyrogram.types import Message
from utilsdf.db import Database

ADMIN_IDS = [123456789]  # Replace with admin IDs

@Client.on_message(filters.command("yourcommand", prefixes=["."]))
async def cmd_your_command(client: Client, m: Message):
    if m.from_user.id not in ADMIN_IDS:
        return
    
    # Your admin logic here
    await m.reply("✅ Command executed")
```

## Submitting Changes

### 1. Test Your Changes
```bash
# Run basic tests
python main.py  # Ensure bot starts

# Test specific functionality
python -m pytest tests/  # If tests exist

# Check code style
black .
flake8 .
```

### 2. Commit Changes
```bash
git add .
git commit -m "feat: add new payment gateway"

# Commit message format:
# feat: new feature
# fix: bug fix
# docs: documentation changes
# style: formatting changes
# refactor: code refactoring
# test: adding tests
# chore: maintenance tasks
```

### 3. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 4. Create Pull Request
- Go to GitHub
- Click "New Pull Request"
- Select your branch
- Fill in the template:
  - Description of changes
  - Testing performed
  - Screenshots (if UI changes)
  - Related issues

### Pull Request Checklist
- [ ] Code follows style guidelines
- [ ] Self-review performed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] No sensitive data committed

## Review Process

1. Automated checks run (if configured)
2. Maintainer reviews code
3. Changes requested (if needed)
4. Approval and merge

## Testing Guidelines

### Unit Tests
```python
import pytest
from gates.your_gate import your_gate

@pytest.mark.asyncio
async def test_your_gate_approved():
    status, msg = await your_gate("4111111111111111", "12", "2025", "123")
    assert status.startswith("Approved")

@pytest.mark.asyncio
async def test_your_gate_invalid():
    status, msg = await your_gate("invalid", "12", "2025", "123")
    assert status.startswith("Dead")
```

### Integration Tests
Test full command flow with test bot token.

## Security Considerations

- **Never commit**:
  - API tokens or keys
  - Session files
  - Database files with user data
  - Real credit card numbers

- **Always**:
  - Use environment variables
  - Validate user input
  - Handle errors gracefully
  - Log without sensitive data

## Documentation

- Update README.md for user-facing changes
- Update INSTALLATION.md for setup changes
- Add docstrings to all functions
- Comment complex logic

## Questions?

- Open an issue for questions
- Join discussions on GitHub
- Check existing issues and PRs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to EliteTestBot Checker! 🎉**
