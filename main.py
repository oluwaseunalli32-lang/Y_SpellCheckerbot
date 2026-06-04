import os
import logging
import asyncio  # 👈 Make sure to import asyncio at the top of your file!
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from spellchecker import SpellChecker

# ... (Keep your logging, spell checker setup, start, and check_spelling functions exactly the same) ...

def main() -> None:
    # Get token from environment variables
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    if not TOKEN:
        logger.error("No TELEGRAM_TOKEN found in environment variables!")
        return

    # Build the application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_spelling))

    # 🛠️ FIX FOR PYTHON 3.14 EVENT LOOP ISSUE:
    logger.info("Y_SpellCheckerbot is starting...")
    
    try:
        # Get the current running event loop
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # If no loop is running, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Run the bot initialization and polling within the loop context
    loop.run_until_complete(application.initialize())
    loop.run_until_complete(application.updater.start_polling())
    loop.run_until_complete(application.start())
    
    # Keep it running until you stop the server
    try:
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        # Clean shutdown
        loop.run_until_complete(application.stop())
        loop.run_until_complete(application.updater.stop())
        loop.run_until_complete(application.shutdown())

if __name__ == "__main__":
    main()
