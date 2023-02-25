import logging

import pyperclip
import telegram
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ApplicationBuilder, MessageHandler, filters

from Functions.ButtonFunctions import get_btn_list, get_pressed_btn
from Functions.Coloring import magenta, red, bright
from Functions.DatabaseCRUD import init as database_init, PERSONS_TABLE, BUTTONS_TABLE, SETTINGS_TABLE, read, add, edit
from MyObjects import Person, Button, SPButton, Setting

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


async def process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    print(magenta('Received Message: ') + update.message.text)
    try:
        parse_mode = None

        # Find person in the database
        persons: list[Person] = read(PERSONS_TABLE, Person, chat_id=user.id)
        if not persons:  # Person is not already registered

            result = add(PERSONS_TABLE, Person(chat_id=user.id,
                                               first_name=user.first_name,
                                               last_name=user.last_name,
                                               username=user.username))

            if result:  # New person added successfully

                persons = read(PERSONS_TABLE, Person, chat_id=user.id)
                if persons:  # Newly added person read successfully
                    person = persons[0]
                    chat_id = person.id
                    reply_markup = ReplyKeyboardMarkup(
                        resize_keyboard=True, keyboard=get_btn_list(person, person.btn_id))
                    text = 'Wellcome to the Bot'
                else:  # Somthing is wrong to read new person
                    chat_id = user.id
                    reply_markup = None
                    text = "Can't find the registered user!"

            else:  # Couldn't add new user!
                chat_id = user.id
                reply_markup = None
                text = "Couldn't add new user!"

        else:  # Person already exists on the database
            person = persons[0]
            chat_id = person.id

            # Knowing pressed key
            pressed_dict = get_pressed_btn(person, update.message.text)
            if pressed_dict:  # Received text was a button

                if not pressed_dict['is_special']:  # Pressed button was nat special
                    pressed_btn: Button = pressed_dict['button']

                    edit(PERSONS_TABLE, id=person.id, btn_id=pressed_btn.id)

                    reply_markup = ReplyKeyboardMarkup(
                        resize_keyboard=True, keyboard=get_btn_list(person, pressed_btn.id))
                    text = update.message.text

                    if pressed_btn.id == 1:
                        text = 'Any text you type in here will be added to your pc clipboard.\n'
                        text += 'Use ((Back)) button to stop.'

                else:  # Pressed button was special

                    pressed_btn: SPButton = pressed_dict['button']
                    if pressed_btn.id == 0:  # Back button pressed

                        last_btns: list[Button] = read(BUTTONS_TABLE, Button, id=person.btn_id)
                        if last_btns:
                            edit(PERSONS_TABLE, id=person.id, btn_id=last_btns[0].belong)
                            reply_markup = ReplyKeyboardMarkup(
                                resize_keyboard=True, keyboard=get_btn_list(person, last_btns[0].belong))
                            text = update.message.text

                        else:  # No way back
                            print('main: ' + red(bright('Wrong belong id')))
                            reply_markup = None
                            text = 'Alert'

                    elif pressed_btn.id == 2:  # Retrieve PC clipboard
                        text = r'Below is the latest text copied by your Pc\. '
                        text += 'You can touch the text once to coppy that on your new device:\n\n'

                        text += "`{copied}`".format(copied=pyperclip.paste().replace("\\", "\\\\").replace("`", r"\`"))
                        parse_mode = 'MarkdownV2'
                        reply_markup = ReplyKeyboardMarkup(
                            resize_keyboard=True, keyboard=get_btn_list(person, person.btn_id))

                    else:
                        reply_markup = ReplyKeyboardMarkup(
                            resize_keyboard=True, keyboard=get_btn_list(person, person.btn_id))
                        text = update.message.text

            else:  # Received text was not a button
                reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=get_btn_list(person, person.btn_id))
                text = update.message.text

                if person.btn_id == 1:
                    pyperclip.copy(text)
                    text = 'Below text added to PC Clipboard: \n\n'
                    text += "`{copied}`".format(copied=pyperclip.paste().replace("\\", "\\\\").replace("`", r"\`"))
                    parse_mode = 'MarkdownV2'

        await context.bot.send_message(
            chat_id if not persons else update.effective_user.id,
            text,
            reply_markup=reply_markup,
            parse_mode=parse_mode)

    except telegram.error.BadRequest as e:
        print('main: ' + red(str(e)))


def main() -> None:
    database_init()
    setting: Setting = read(SETTINGS_TABLE, Setting, name='BOT_TOKEN')[0]
    if setting.value:
        token = setting.value
    else:
        text = input('Please write your bot token here:\n')
        token = text
        edit(SETTINGS_TABLE, id=setting.id, value=token)

    application = ApplicationBuilder().token(token).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), process))
    try:
        application.run_polling()
    except telegram.error.TimedOut as e:
        print(f'main: {red(str(e))}')
    except telegram.error.InvalidToken as e:
        print(f'main: {red(str(e))}')
        edit(SETTINGS_TABLE, id=setting.id, value=None)


if __name__ == '__main__':
    main()
