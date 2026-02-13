# bot.py
import os
import logging
import signal
import sys
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Read environment variables (names must match exactly in Render)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Debug check (prints only presence/length, never the token itself)
if TELEGRAM_TOKEN:
    logger.info("TELEGRAM_TOKEN is present; length: %d", len(TELEGRAM_TOKEN))
else:
    raise ValueError("TELEGRAM_TOKEN is missing. Add it in Render → Environment.")

if not GROQ_API_KEY:
    logger.warning("GROQ_API_KEY is not set. If your bot needs it, add it in Render → Environment.")

# Handlers
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Bot is running.")

def echo(update: Update, context: CallbackContext):
    text = update.message.text or ""
    update.message.reply_text(text)

def error_handler(update: object, context: CallbackContext):
    logger.exception("Exception while handling an update: %s", context.error)

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()
    logger.info("Bot started polling.")

    # Graceful shutdown on SIGTERM (Render sends SIGTERM before stopping)
    def shutdown(signum, frame):
        logger.info("Shutdown signal received (%s). Stopping bot...", signum)
        updater.stop()
        updater.is_idle = False

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    # Block until the bot is stopped
    updater.idle()
    logger.info("Bot stopped.")

if __name__ == "__main__":
    main()
