# Verification Bot via Telegram

A Discord-Telegram verification bot that provides secure server access through a two-step verification process. Users receive a verification code through Telegram and verify themselves in Discord to gain access to the server.

## Features

- 🔐 Secure two-step verification process
- 🤖 Integration with both Discord and Telegram
- 🎯 Automatic role assignment upon verification
- 📝 Customizable welcome messages
- 🔢 6-digit verification codes
- ⚡ Fast and easy to use

## Setup

1. Create a `.env` file with the following variables:
```env
DISCORD_TOKEN=your_discord_bot_token
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
ROLE=your_discord_role_id
WELCOME_MESSAGE="Welcome {user}! You have been successfully verified! Enjoy your stay!"
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the bot:
```bash
python main.py
```

## How to Use

### For Users
1. **Telegram**: 
   - Find the Telegram bot and start a chat
   - Type `/verify` to receive a verification code
   - You will receive a 6-digit code

2. **Discord**:
   - Go to the Discord server
   - Type `/code <your-6-digit-code>`
   - Upon successful verification, you'll receive the verified role

### For Admins
1. Make sure the bot has proper permissions in your Discord server
2. Set up the verified role ID in the `.env` file
3. Customize the welcome message as needed

## Requirements
- Python 3.8 or higher
- discord.py
- python-telegram-bot
- python-dotenv

## Support
If you encounter any issues or need help, please open an issue in the repository.

## License
This project is licensed under the MIT License - see the LICENSE file for details