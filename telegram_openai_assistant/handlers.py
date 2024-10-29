# handlers.py
import time
import datetime
from telegram.ext import CallbackContext
from telegram import Update
from openai import OpenAI
from dotenv import load_dotenv
import os

from .config import assistant_id, client_api_key
from .utils import get_message_count, update_message_count, save_qa

# Список разрешённых Telegram ID
load_dotenv()
ALLOWED_USERS = set(int(user_id) for user_id in os.getenv("ALLOWED_USERS", "").split(",") if user_id.strip())

client = OpenAI(api_key=client_api_key)


async def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message to the user."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Привет! Это ассистент ЦИПиК, у меня можно спросить про Инфостарт."
    )


async def help_command(update: Update, context: CallbackContext) -> None:
    """Sends a help message to the user."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Отправь мне вопрос и я постараюсь на него ответить.",
    )


def get_answer(message_str) -> None:
    """Get answer from assistant"""
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=message_str
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(run.status)
        if run.status == "completed":
            break
        time.sleep(1)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = messages.dict()["data"][0]["content"][0]["text"]["value"]
    return response


# Функция проверки доступа
def check_user_access(user_id):
    return user_id in ALLOWED_USERS


async def process_message(update: Update, context: CallbackContext) -> None:
    """Processes a message from the user, gets an answer, and sends it back."""
    message_data = get_message_count()
    count = message_data["count"]
    date = message_data["date"]
    today = str(datetime.date.today())

    if date != today:
        count = 0
    if count >= 100:
        return

    user_id = update.effective_user.id
    if not check_user_access(user_id):
        await update.message.reply_text("У вас нет доступа к этому боту.")
        return
    else:
        answer = get_answer(update.message.text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
        update_message_count(count + 1)
        save_qa(
            update.effective_user.id,
            update.effective_user.username,
            update.message.text,
            answer,
        )
