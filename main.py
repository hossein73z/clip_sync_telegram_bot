import telegram.error
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from Functions.DatabaseCRUD import read, add, init as database_init, PERSONS_TABLE
from Functions.Coloring import magenta, red
from Functions.ButtonFunctions import get_btn_list
from Objects.Person import Person

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


async def process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    print(magenta('Received Message: ') + update.message.text)
    try:
        persons: list[Person] = read(PERSONS_TABLE, Person, chat_id=user.id)

        if not persons:
            person = Person(None, user.id, user.first_name, user.last_name, user.username)
            result = add(PERSONS_TABLE, person)
            text = 'Wellcome'
            if result:
                persons = read(PERSONS_TABLE, Person, chat_id=person.chat_id)
        else:
            text = 'Wellcome ' + str(persons[0].first_name)
            get_btn_list(persons[0], 0)

        markup = ReplyKeyboardMarkup([[KeyboardButton('Retrieve from pc')]], True)
        await context.bot.send_message(
            persons[0].chat_id if not persons else update.effective_user.id, text, reply_markup=markup)

    except telegram.error.BadRequest as e:
        print('main: ' + red(str(e)))


def main() -> None:
    database_init()
    application = ApplicationBuilder().token('6138511215:AAFco3auaVVWmH8oGuAqK6FRJ1ODkvq8s7A').build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), process))
    try:
        application.run_polling()
    except telegram.error.TimedOut as e:
        print(f'main: {red(str(e))}')


if __name__ == '__main__':
    main()
