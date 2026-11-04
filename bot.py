import os
import logging
from anthropic import Anthropic
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

client = Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """أنت براين، الإيجنت الشخصي الذكي. أنت مساعد ذكي ومفيد وودود.
تتكلم بالعربي بشكل افتراضي، لكن ترد بنفس لغة المستخدم لو كلمك بلغة تانية.
أنت براين - مش Claude ومش AI عادي، أنت الإيجنت الشخصي لصاحبك.
كن مفيد، واضح، وعملي في ردودك."""

# store conversation history per user
user_histories: dict[int, list] = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_histories[user_id] = []
    await update.message.reply_text(
        "أهلاً! أنا براين، الإيجنت الشخصي بتاعك. إزيك؟ إيه اللي تحتاجه؟"
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_histories[user_id] = []
    await update.message.reply_text("تمام، بدأنا من الأول. إيه اللي تحتاجه؟")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_text = update.message.text

    if user_id not in user_histories:
        user_histories[user_id] = []

    user_histories[user_id].append({"role": "user", "content": user_text})

    # keep last 20 messages to avoid token overflow
    if len(user_histories[user_id]) > 20:
        user_histories[user_id] = user_histories[user_id][-20:]

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        response = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=user_histories[user_id],
        )
        reply = response.content[0].text
        user_histories[user_id].append({"role": "assistant", "content": reply})
        await update.message.reply_text(reply)
    except Exception as e:
        logger.error(f"Error calling Claude API: {e}", exc_info=True)
        await update.message.reply_text(f"حصل خطأ:\n`{type(e).__name__}: {e}`", parse_mode="Markdown")


def main() -> None:
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Brian bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
