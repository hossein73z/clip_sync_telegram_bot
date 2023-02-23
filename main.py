import logging

import telegram
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ApplicationBuilder, MessageHandler, filters

from Functions.ButtonFunctions import get_btn_list, get_pressed_btn
from Functions.Coloring import magenta, red, bright
from Functions.DatabaseCRUD import init as database_init, PERSONS_TABLE, BUTTONS_TABLE, read, add, edit
from MyObjects import Person, Button, SPButton

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


async def process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    print(magenta('Received Message: ') + update.message.text)
    try:

        # Find person in the database
        persons: list[Person] = read(PERSONS_TABLE, Person, chat_id=user.id)
        if not persons:
            # Person is not already registered

            result = add(PERSONS_TABLE, Person(chat_id=user.id,
                                               first_name=user.first_name,
                                               last_name=user.last_name,
                                               username=user.username))
            if result:
                # New person added successfully

                persons = read(PERSONS_TABLE, Person, chat_id=user.id)
                if persons:
                    # Newly added person read successfully

                    person = persons[0]
                    chat_id = person.id
                    reply_markup = ReplyKeyboardMarkup(
                        resize_keyboard=True, keyboard=get_btn_list(person, person.btn_id))
                    text = 'Wellcome to the Bot'
                else:
                    # Somthing is wrong to read new person

                    chat_id = user.id
                    reply_markup = None
                    text = "Can't find the registered user!"
            else:
                # Couldn't add new user!

                chat_id = user.id
                reply_markup = None
                text = "Couldn't add new user!"
        else:
            # Person already exists on the database

            person = persons[0]
            chat_id = person.id

            # Knowing pressed key
            pressed_dict = get_pressed_btn(person, update.message.text)
            if pressed_dict:
                # Received text was a button

                if not pressed_dict['is_special']:
                    # Pressed button was nat special
                    pressed_btn: Button = pressed_dict['button']

                    edit(PERSONS_TABLE, id=person.id, btn_id=pressed_btn.id)
                    # Person updated successfully

                    reply_markup = ReplyKeyboardMarkup(
                        resize_keyboard=True, keyboard=get_btn_list(person, pressed_btn.id))
                    text = update.message.text

                    # Somthing went wrong during updating person
                    # print('main: ' + red(bright('Person not updated!')))
                    # reply_markup = None
                    # text = 'Alert'

                else:
                    # Pressed button was special
                    pressed_btn: SPButton = pressed_dict['button']

                    if pressed_btn.id == 0:
                        # Back button pressed

                        last_btns: list[Button] = read(BUTTONS_TABLE, Button, id=person.btn_id)
                        if last_btns:
                            edit(PERSONS_TABLE, id=person.id, btn_id=last_btns[0].belong)
                            reply_markup = ReplyKeyboardMarkup(
                                resize_keyboard=True, keyboard=get_btn_list(person, last_btns[0].belong))
                            text = update.message.text
                        else:
                            # No way back

                            print('main: ' + red(bright('Wrong belong id')))
                            reply_markup = None
                            text = 'Alert'
                    else:
                        reply_markup = None
                        text = update.message.text

            else:
                # Received text was not a button

                reply_markup = ReplyKeyboardMarkup(
                    resize_keyboard=True, keyboard=get_btn_list(person, person.btn_id))
                text = update.message.text

        await context.bot.send_message(
            chat_id if not persons else update.effective_user.id, text, reply_markup=reply_markup)

    except telegram.error.BadRequest as e:
        print('main: ' + red(str(e)))


def main() -> None:
    database_init()
    application = ApplicationBuilder().token('6138511215:AAGwo0MQGYXOUBgNhA_TxvwH2xpxnQgb_-I').build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), process))
    try:
        application.run_polling()
    except telegram.error.TimedOut as e:
        print(f'main: {red(str(e))}')


if __name__ == '__main__':
    main()
