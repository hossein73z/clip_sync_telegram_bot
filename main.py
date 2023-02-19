import os
import telegram.error
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import pyperclip
from Functions.DatabaseCRUD import Database
from Functions.Coloring import magenta, red
from Objects.Person import Person

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
database = Database()


async def process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    print(magenta('Received Message: ') + update.message.text)
    try:
        persons: list[Person] = database.read(database.PERSONS, Person, chat_id=user.id)

        if not persons:
            person = Person(None, user.id, user.first_name, user.last_name, user.username)
            result = database.add(database.PERSONS, person)
            text = 'Wellcome'
            if result:
                persons = database.read(database.PERSONS, Person, chat_id=person.chat_id)
        else:
            text = 'Wellcome ' + str(persons[0].first_name)

        markup = ReplyKeyboardMarkup([[KeyboardButton('Retrieve from pc')]], True)
        await context.bot.send_message(
            persons[0].chat_id if not persons else update.effective_user.id, text, reply_markup=markup)

    except telegram.error.BadRequest as e:
        print('main: ' + red(str(e)))


def main() -> None:
    application = ApplicationBuilder().token('6138511215:AAFco3auaVVWmH8oGuAqK6FRJ1ODkvq8s7A').build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), process))
    try:
        application.run_polling()
    except telegram.error.TimedOut as e:
        print(f'main: {red(str(e))}')


if __name__ == '__main__':
    main()
