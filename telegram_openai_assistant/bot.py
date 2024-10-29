from telegram.ext import Application, CommandHandler, MessageHandler, filters
from .config import telegram_token
from .handlers import start, help_command, process_message, check_user_access
import os
import requests


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

application = Application.builder().token(telegram_token).build()

# Обработчик команды save
async def update_knowledge(update, context):
    user_id = update.effective_user.id
    if not check_user_access(user_id):
        await update.message.reply_text("У вас нет доступа к этому боту.")
        return
    
    # Получаем текст, который необходимо сохранить
    message_text = ' '.join(context.args)
    if not message_text:
        await update.message.reply_text("Пожалуйста, укажите текст для сохранения:\n/add Факт")
        return

    # Записываем текст в файл
    with open("custom_knowledge_file.txt", "a") as file:
        file.write(message_text + "\n")
    
    # Отправка файла на OpenAI Assistants API 
    with open("custom_knowledge_file.txt", "rb") as file:
        url = "https://api.openai.com/v1/vector_stores/vs_aZl8dFZFiDX01UOZfJTvKzHk"
        headers = {
            "Authorization": f"Bearer {os.getenv('CLIENT_API_KEY')}",  # Замените на ваш ключ API
            "Content-Type": "application/json",
            "OpenAI-Beta": "assistants=v2"
        }
        # Подготовьте данные в формате, который ожидает OpenAI API
        data = {
            "metadata": {
                "author": "kapatsahelen",
                "message": str(update.message.date)   
            }
        }

        response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        await update.message.reply_text("Текст успешно сохранён и отправлен.")
    else:
        await update.message.reply_text(f"Ошибка при отправке: {response.text}")


def setup_handlers(app):
    """Sets up the command and message handlers for the bot."""
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", update_knowledge))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

def main():
    """Main function to run the bot."""
    setup_handlers(application)
    application.run_polling()

if __name__ == "__main__":
    main()
