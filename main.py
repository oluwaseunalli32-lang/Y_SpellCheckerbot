import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from spellchecker import SpellChecker

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize the spell checker
spell = SpellChecker()

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Hello! I am Y_SpellCheckerbot.\n\n"
        "Send me any text, and I will automatically check it for spelling errors!"
    )

# Text processor and spell checker logic
async def check_spelling(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    
    # Skip checking if it looks like a command
    if text.startswith('/'):
        return

    # Clean the text into words
    words = spell.split_words(text)
    misspelled = spell.unknown(words)

    if not misspelled:
        # Optional: You can remove this if you don't want the bot replying to perfectly written texts.
        # await update.message.reply_text("✅ No spelling errors found!")
        return

    # Build the correction message
    correction_message = "📝 **Spelling Suggestions:**\n\n"
    for word in misspelled:
        correct_word = spell.correction(word)
        if correct_word and correct_word != word:
            correction_message += f"❌ *{word}* ➡️ ✨ *{correct_word}*\n"

    await update.message.reply_text(correction_message, parse_mode="Markdown")

def main() -> None:
    # Get token from environment variables (Render will provide this)
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    if not TOKEN:
        logger.error("No TELEGRAM_TOKEN found in environment variables!")
        return

    # Build the application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_spelling))

    # Start the bot using polling
    logger.info("Y_SpellCheckerbot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
