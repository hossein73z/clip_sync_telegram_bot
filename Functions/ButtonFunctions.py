from telegram import KeyboardButton

from Functions.DatabaseCRUD import BUTTONS_TABLE, SP_BUTTONS_TABLE, read
from MyObjects import Person, Button, SPButton


def get_btn_list(person: Person, button_id: int):
    # Get all the buttons from database
    raw_btns: list[Button] = read(BUTTONS_TABLE, Button, admin=person.admin)
    raw_sp_btns: list[SPButton] = read(SP_BUTTONS_TABLE, SPButton, admin=person.admin)

    # Create dictionary with buttons and their ids
    buttons_dict: {int, Button} = {b.id: b for b in raw_btns} if raw_btns else None
    sp_buttons_dict: {int, SPButton} = {b.id: b for b in raw_sp_btns} if raw_sp_btns else None

    if buttons_dict:
        button = buttons_dict[button_id]
        # Create array arrays of keyboard button for telegram reply markup
        buttons___ = [[KeyboardButton(text=buttons_dict[b_id].text) for b_id in ids]
                      for ids in button.btns] if button.btns and buttons_dict else []

        # Create array arrays of special keyboard button for telegram reply markup
        sp_buttons = [[KeyboardButton(text=sp_buttons_dict[b_id].text) for b_id in ids]
                      for ids in button.sp_btns] if button.sp_btns and sp_buttons_dict else []

        return buttons___ + sp_buttons

    else:
        return None


def get_pressed_btn(person: Person, text: str):
    # Get pressed button from database
    raw_btns: list[Button] = read(BUTTONS_TABLE, Button, admin=person.admin, belong=person.btn_id, text=text)

    if raw_btns:  # Received text was a normal button. Returning
        return {'button': raw_btns[0], 'is_special': False}

    else:  # Received text was not a normal button

        last_btns: list[Button] = read(BUTTONS_TABLE, Button, admin=person.admin, id=person.btn_id)
        ids = [item for items in last_btns[0].sp_btns for item in items]  # Create a list of ids from nested list

        if ids:
            # Find pressed button using text and id list
            sp_btns = read(SP_BUTTONS_TABLE, SPButton, admin=person.admin, id=set(ids), text=text)
            if sp_btns:
                return {'button': sp_btns[0], 'is_special': True}
