"""
Telegram-бот для RAG-пайплайна Veylarian Chronicles.

Использование:
    export OPENAI_API_KEY=sk-...
    export TELEGRAM_BOT_TOKEN=123456:ABC-...
    python task4/telegram_bot.py
"""

import logging
import os
import sys

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Добавляем task4/ в path для импорта rag_chain
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rag_chain import RAGBot

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Глобальный экземпляр бота — инициализируется один раз при старте
rag_bot: RAGBot | None = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I'm the Veylarian Chronicles knowledge bot.\n\n"
        "Ask me anything about the Veylarian universe — characters, "
        "planets, technology, factions, events.\n\n"
        "Example: Who is Kael Venarix?"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text.strip()
    if not question:
        return

    logger.info(f"Question from {update.effective_user.id}: {question}")
    await update.message.chat.send_action("typing")

    try:
        result = rag_bot.ask_with_sources(question)
        answer = result["answer"]
        sources = ", ".join(s["file"] for s in result["sources"])
        response = f"{answer}\n\n📚 Sources: {sources}"
    except Exception as e:
        logger.error(f"Error: {e}")
        response = "Sorry, an error occurred while processing your question."

    await update.message.reply_text(response)


def main():
    global rag_bot

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is not set.")
        print("1. Create a bot via @BotFather in Telegram")
        print("2. Export the token: export TELEGRAM_BOT_TOKEN=123456:ABC-...")
        sys.exit(1)

    # Инициализация RAG (загрузка модели + индекса)
    rag_bot = RAGBot()

    # Запуск Telegram-бота
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("\nTelegram bot is running. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
