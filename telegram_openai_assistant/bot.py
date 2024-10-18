from telegram.ext import Application, CommandHandler, MessageHandler, filters
from .config import telegram_token
from .handlers import start, help_command, process_message
import os
from dotenv import load_dotenv


load_dotenv()

# Список разрешённых Telegram ID
ALLOWED_USERS = set(int(user_id) for user_id in os.getenv("ALLOWED_USERS", "").split(",") if user_id.strip())

# Функция проверки доступа
def check_user_access(user_id):
    return user_id in ALLOWED_USERS

# Обработчик команды start
async def start(update, context):
    user_id = update.effective_user.id
    if not check_user_access(user_id):
        await update.message.reply_text("У вас нет доступа к этому боту.")
        return
    await update.message.reply_text("Добро пожаловать!")

# Обработчик команды help
async def help_command(update, context):
    user_id = update.effective_user.id
    if not check_user_access(user_id):
        await update.message.reply_text("У вас нет доступа к этому боту.")
        return
    await update.message.reply_text("Список доступных команд...")

# Обработчик сообщений
async def process_message(update, context):
    user_id = update.effective_user.id
    if not check_user_access(user_id):
        await update.message.reply_text("У вас нет доступа к этому боту.")
        return
    # Обработка сообщений для разрешённых пользователей
    await update.message.reply_text("Ваше сообщение обработано.")

application = Application.builder().token(telegram_token).build()

def setup_handlers(app):
    """Sets up the command and message handlers for the bot."""
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

def main():
    """Main function to run the bot."""
    setup_handlers(application)
    application.run_polling()

if __name__ == "__main__":
    main()
