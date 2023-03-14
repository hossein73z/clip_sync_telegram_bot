import json

import pyperclip
import telegram
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters

from Functions.ButtonFunctions import get_btn_list, get_pressed_btn
from Functions.Coloring import magenta, red, bright
from Functions.DatabaseCRUD import init, read, add, edit
from MyObjects import Person, Button, SPButton, Setting


async def process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    print(magenta('Received Message: ') + update.message.text)
    try:
        parse_mode = None

        # Find person in the database
        persons: list[Person] = read(Person, chat_id=user.id)
        if not persons:  # Person is not already registered
            admins: list[Person] = read(Person, admin=1)
            if not admins:  # There is no admin registered on database
                result = add(Person(chat_id=user.id,
                                    first_name=user.first_name,
                                    last_name=user.last_name if user.last_name else None,
                                    admin=1,
                                    username=user.username))

                if result:  # New person added successfully

                    persons = read(Person, chat_id=user.id)
                    if persons:  # Newly added person read successfully
                        person = persons[0]
                        chat_id = person.id
                        reply_markup = ReplyKeyboardMarkup(
                            resize_keyboard=True, keyboard=get_btn_list(admin=person.admin, button_id=person.btn_id))
                        text = 'Wellcome to the Bot'

                        await context.bot.send_message(
                            chat_id if not persons else update.effective_user.id,
                            text,
                            reply_markup=reply_markup,
                            parse_mode=parse_mode)

                    else:  # Somthing is wrong to read new person
                        chat_id = user.id
                        reply_markup = None
                        text = "Can't find the registered user!"

                        await context.bot.send_message(
                            chat_id if not persons else update.effective_user.id,
                            text,
                            reply_markup=reply_markup,
                            parse_mode=parse_mode)

                else:  # Couldn't add new user!
                    chat_id = user.id
                    reply_markup = None
                    text = "Couldn't add new user!"

                    await context.bot.send_message(
                        chat_id if not persons else update.effective_user.id,
                        text,
                        reply_markup=reply_markup,
                        parse_mode=parse_mode)

            else:  # There is at least one admin registered on database
                add(Person(id=None,
                           chat_id=user.id,
                           first_name=user.first_name,
                           last_name=user.last_name,
                           username=user.username,
                           progress={"name": "JOIN", "value": {"status": "waiting"}}))
                person: Person = read(Person, chat_id=user.id)[0]

                keyboard = [[
                    InlineKeyboardButton(
                        text="Accept",
                        callback_data=json.dumps({'name': 'JOIN_REQ', 'value': {'status': 'ACC', 'id': person.id}})),
                    InlineKeyboardButton(
                        text="Reject",
                        callback_data=json.dumps({'name': 'JOIN_REQ', 'value': {'status': 'REJ', 'id': person.id}}))
                ]]
                reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
                text = 'New person is requesting to use this bot.\n'
                text += f'Name: {user.first_name} {user.last_name if user.last_name else ""}\n'
                text += f'Username: @{user.username if user.username else ""} ('
                text = text.replace("\\", "\\\\").replace("`", r"\`").replace(r'.', r'\.').replace('(', r'\(')
                text += f"[Profile](tg://user?id={user.id})" + r"\)"
                print(text)

                for admin in admins:
                    await context.bot.send_message(
                        admin.chat_id,
                        text,
                        reply_markup=reply_markup,
                        parse_mode='MarkdownV2')

                await context.bot.send_message(
                    user.id,
                    'Your request for using this bot has been sent to admin. Please be patient',
                    reply_markup=None,
                    parse_mode=parse_mode)

        else:  # Person already exists on the database
            person = persons[0]
            person.first_name = user.first_name
            person.last_name = user.last_name
            person.username = user.username
            edit(Person, id=person.id, first_name=person.first_name, last_name=person.last_name,
                 username=person.username)
            chat_id = person.id

            joined = True
            try:
                text = 'Hi'
                if person.progress:
                    if person.progress['name'] == 'JOIN' and person.progress['value']['status'] == 'accepted':
                        joined = True
                    elif person.progress['name'] == 'JOIN' and person.progress['value']['status'] == 'waiting':
                        joined = False
                        text = 'Please stand by.'
                    elif person.progress['name'] == 'JOIN' and person.progress['value']['status'] == 'rejected':
                        joined = False
                        text = 'You do not have permission to use this bot'
            except TypeError or KeyError or IndexError as e:
                text = 'Error'
                print('main: ' + red(str(e)))

            if joined:
                # Finding pressed key
                pressed_dict = get_pressed_btn(person.btn_id, person.admin, update.message.text)

                if pressed_dict:  # Received text was a button

                    if not pressed_dict['is_special']:  # Pressed button was nat special
                        pressed_btn: Button = pressed_dict['button']

                        edit(Person, id=person.id, btn_id=pressed_btn.id)

                        reply_markup = ReplyKeyboardMarkup(
                            resize_keyboard=True, keyboard=get_btn_list(admin=person.admin, button_id=pressed_btn.id))

                        if pressed_btn.messages:  # Pressed button has predefined message(s)
                            messages = pressed_btn.messages

                            for message in messages:
                                text = message.text
                                await context.bot.send_message(
                                    chat_id if not persons else update.effective_user.id,
                                    text,
                                    reply_markup=reply_markup,
                                    parse_mode=parse_mode)

                        else:  # Pressed button has no message registered on the database
                            text = update.message.text
                            await context.bot.send_message(
                                chat_id if not persons else update.effective_user.id,
                                text,
                                reply_markup=reply_markup,
                                parse_mode=parse_mode)

                    else:  # Pressed button was special

                        pressed_btn: SPButton = pressed_dict['button']
                        if pressed_btn.id == 0:  # Back button pressed

                            last_btns: list[Button] = read(Button, id=person.btn_id)
                            if last_btns:
                                edit(Person, id=person.id, btn_id=last_btns[0].belong)
                                reply_markup = ReplyKeyboardMarkup(
                                    resize_keyboard=True,
                                    keyboard=get_btn_list(admin=person.admin, button_id=last_btns[0].belong))
                                text = update.message.text

                            else:  # No way back
                                print('main: ' + red(bright('Wrong belong id')))
                                reply_markup = None
                                text = 'Alert'

                        elif pressed_btn.id == 2:  # Retrieve PC clipboard
                            text = r'Below is the latest text copied by your Pc\. '
                            text += 'You can touch the text once to coppy that on your new device:\n\n'

                            text += "`{copied}`".format(
                                copied=pyperclip.paste().replace("\\", "\\\\").replace("`", r"\`"))
                            parse_mode = 'MarkdownV2'
                            reply_markup = ReplyKeyboardMarkup(
                                resize_keyboard=True,
                                keyboard=get_btn_list(admin=person.admin, button_id=person.btn_id))

                        else:
                            reply_markup = ReplyKeyboardMarkup(
                                resize_keyboard=True,
                                keyboard=get_btn_list(admin=person.admin, button_id=person.btn_id))
                            text = update.message.text

                        await context.bot.send_message(
                            chat_id if not persons else update.effective_user.id,
                            text,
                            reply_markup=reply_markup,
                            parse_mode=parse_mode)

                else:  # Received text was not a button
                    reply_markup = ReplyKeyboardMarkup(
                        resize_keyboard=True, keyboard=get_btn_list(admin=person.admin, button_id=person.btn_id))
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
            else:
                print(chat_id if not persons else update.effective_user.id)
                await context.bot.send_message(
                    chat_id if not persons else update.effective_user.id,
                    text,
                    reply_markup=ReplyKeyboardRemove(),
                    parse_mode=parse_mode)

    except telegram.error.BadRequest as e:
        print('main: ' + red(str(e)))


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    # {'name': 'JOIN_REQ', 'value': {'status': 'ACC', 'id': person.id}}
    data = json.loads(query.data)
    if data['name'] == 'JOIN_REQ':  # Join new user status response
        persons = read(Person, id=data['value']['id'])

        if persons:
            person: Person = persons[0]
            try:
                if person.progress['value']['status'] == 'waiting':  # The user still waiting for approval

                    if data['value']['status'] == 'ACC':  # Join new user accepted
                        progress = person.progress
                        progress['value']['status'] = 'accepted'
                        edit(Person, id=person.id, progress=json.dumps(progress))

                        text = query.message.text
                        text.replace('New person is requesting to use this bot', 'New user added successfully')
                        await query.answer(text='Accepted')
                        await query.edit_message_text(text=text, reply_markup=None)
                        await context.bot.send_message(
                            chat_id=person.chat_id,
                            text='Your permission accepted',
                            reply_markup=ReplyKeyboardMarkup(get_btn_list(admin=0, button_id=0), resize_keyboard=True))

                    elif data['value']['status'] == 'REJ':  # Join new user rejected
                        progress = person.progress
                        progress['value']['status'] = 'rejected'
                        edit(Person, id=person.id, progress=json.dumps(progress))

                        text = query.message.text
                        text.replace('New person is requesting to use this bot', 'Permission denied')
                        await query.answer(text='Rejected')
                        await query.edit_message_text(text=text, reply_markup=None)
                        await context.bot.send_message(
                            chat_id=person.chat_id,
                            text='Permission denied',
                            reply_markup=ReplyKeyboardRemove())

                else:
                    text = 'Expired'
                    try:
                        text = 'Request already accepted by other admins' \
                            if person.progress['value']['status'] == 'accepted' \
                            else 'Request already rejected by other admins'
                    except IndexError as e:
                        print('button: ' + red(str(e)))
                    finally:
                        await query.answer(text)
                        await query.message.delete()

            except IndexError as e:
                print('button: ' + red(str(e)))


def main() -> None:
    init()
    setting: Setting = read(Setting, name='BOT_TOKEN')[0]
    if setting.value:
        token = setting.value
    else:
        text = input('Please write your bot token here:\n')
        token = text
        edit(Setting, id=setting.id, value=token)

    application = ApplicationBuilder().token(token).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), process))
    application.add_handler(CallbackQueryHandler(button))
    try:
        application.run_polling()
    except telegram.error.TimedOut as e:
        print(f'main: {red(str(e))}')
    except telegram.error.InvalidToken as e:
        print(f'main: {red(str(e))}')
        edit(Setting, id=setting.id, value=None)


if __name__ == '__main__':
    main()
