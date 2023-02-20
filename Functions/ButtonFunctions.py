from Functions.Coloring import red, magenta, yellow
from Objects.Person import Person
from Objects.Buttton import Button
from Objects.SPButtton import SPButton
from Functions.DatabaseCRUD import read, SP_BUTTONS_TABLE, BUTTONS_TABLE

from telegram import KeyboardButton


def get_btn_list(person: Person, button_id):
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
