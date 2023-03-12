from telegram import KeyboardButton

from Functions.DatabaseCRUD import read
from MyObjects import Person, Button, SPButton


def get_btn_list(person_btn_id: int, admin: int, button_id: int):
    """
    Get all the buttons from database

    :param person_btn_id:ID of person's last pressed button
    :param admin: Person administration level
    :param button_id: ID of the button to get its subset buttons
    :return: array of array of KeyboardButton object or None if there's no subset buttons
    """

    raw_btns: list[Button] = read(Button, admin=set(range(0, admin + 1)))
    raw_sp_btns: list[SPButton] = read(SPButton, admin=set(range(0, admin + 1)))

    # Create dictionaries with buttons and their ids
    buttons_dict: {int, Button} = {b.id: b for b in raw_btns} if raw_btns else None
    sp_buttons_dict: {int, SPButton} = {b.id: b for b in raw_sp_btns} if raw_sp_btns else None

    if buttons_dict:
        button = buttons_dict[button_id]
        # Create array of array of keyboard button for telegram reply markup
        buttons___ = [[KeyboardButton(text=buttons_dict[b_id].text) for b_id in ids]
                      for ids in button.btns] if button.btns and buttons_dict else []

        # Create array of array of special keyboard button for telegram reply markup
        sp_buttons = [[KeyboardButton(text=sp_buttons_dict[b_id].text) for b_id in ids]
                      for ids in button.sp_btns] if button.sp_btns and sp_buttons_dict else []

        return buttons___ + sp_buttons

    else:
        return None


def get_pressed_btn(person_btn_id: int, admin: int, text: str) -> dict | None:
    """
    find and return pressed button from database based on the received text and last pressed button

    :param person_btn_id:ID of person's last pressed button
    :param admin: Person administration level
    :param text: text of the wanted button.
    :return: dict:{'button': <Pressed_button>, 'is_special': <bool>} if the text matches a button and None otherwise.
    """
    raw_btns: list[Button] = read(Button,
                                  admin=set(range(0, admin + 1)),
                                  belong=person_btn_id,
                                  text=text)

    if raw_btns:  # Received text was a normal button. Returning

        return {'button': raw_btns[0], 'is_special': False}
    else:  # Received text was not a normal button

        last_btns: list[Button] = read(Button,
                                       admin=set(range(0, admin + 1)),
                                       id=person_btn_id)
        if last_btns[0].sp_btns:
            ids = [item for items in last_btns[0].sp_btns for item in items]  # Create a list of ids from nested list
        else:
            ids = None

        if ids:
            # Find pressed button using text and id list
            sp_btns = read(SPButton, admin=set(range(0, admin + 1)), id=set(ids), text=text)
            if sp_btns:  # Match found. Returning the value
                return {'button': sp_btns[0], 'is_special': True}

            else:  # No button matched id-text combination
                return None

        else:  # The last button have no special button
            return None
