import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from spellchecker import SpellChecker

# 1. Setup Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2. Initialize Spell Checker
spell = SpellChecker()

# 3. Define Handlers FIRST (Fixes the NameError)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Hello! I am Y_SpellCheckerbot.\n\n"
        "Send me any text, and I will automatically check it for spelling errors!"
    )

async def check_spelling(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    
    if text.startswith('/'):
        return

    words = spell.split_words(text)
    misspelled = spell.unknown(words)

    if not misspelled:
        return

    correction_message = "📝 **Spelling Suggestions:**\n\n"
    for word in misspelled:
        correct_word = spell.correction(word)
        if correct_word and correct_word != word:
            correction_message += f"❌ *{word}* ➡️ ✨ *{correct_word}*\n"

    await update.message.reply_text(correction_message, parse_mode="Markdown")

# 4. Main Function LAST
def main() -> None:
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    if not TOKEN:
        logger.error("No TELEGRAM_TOKEN found in environment variables!")
        return

    application = Application.builder().token(TOKEN).build()

    # These will now work perfectly because 'start' and 'check_spelling' are defined above!
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_spelling))

    logger.info("Y_SpellCheckerbot is starting...")
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(application.initialize())
    loop.run_until_complete(application.updater.start_polling())
    loop.run_until_complete(application.start())
    
    try:
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.run_until_complete(application.stop())
        loop.run_until_complete(application.updater.stop())
        loop.run_until_complete(application.shutdown())

if __name__ == "__main__":
    main()
