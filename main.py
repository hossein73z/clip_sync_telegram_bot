import os
import logging

import telegram.error
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import pyperclip

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message.text)
    user_id = os.environ.get('ADMIN_ID', '')
    if update.message.text == 'Retrieve from pc':
        text = pyperclip.paste()

    else:
        if not user_id:
            text = 'You are registered as admin and can use this bot'
            os.environ.setdefault('ADMIN_ID', str(update.effective_user.id))
            user_id = os.environ.get('ADMIN_ID', '')
        elif update.effective_user.id != int(user_id):
            text = 'This bot is built for personal use and only admin can use it.'
            print(user_id)
        else:
            pyperclip.copy(update.message.text)
            text = 'Message Received!'

    markup = ReplyKeyboardMarkup([[KeyboardButton('Retrieve from pc')]], True)
    await context.bot.send_message(user_id, text, reply_markup=markup)

    try:
        pass
    except telegram.error.BadRequest:
        print('Message text is empty')


def main() -> None:
    application = ApplicationBuilder().token('6138511215:AAFco3auaVVWmH8oGuAqK6FRJ1ODkvq8s7A').build()

    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), process))

    application.run_polling()


if __name__ == '__main__':
    main()
