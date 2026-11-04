# Brian - Personal AI Agent

براين هو الإيجنت الشخصي على تليجرام، مبني على Claude AI.

## Commands
- `/start` - بدء المحادثة
- `/reset` - مسح تاريخ المحادثة والبدء من الأول

## Deploy on Railway

1. ادفع الكود على GitHub
2. روح على [railway.app](https://railway.app) وعمل New Project من الريبو
3. في Variables أضف:
   - `TELEGRAM_BOT_TOKEN` = توكن البوت من BotFather
   - `ANTHROPIC_API_KEY` = مفتاح Anthropic API

## Run Locally

```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN=your_token
export ANTHROPIC_API_KEY=your_key
python bot.py
```
