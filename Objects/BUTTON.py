import json
from Functions.Coloring import red
from Objects.MyObject import MyObject


class BUTTON(MyObject):
    button_id: int = 0
    text: str = ''
    admin_key: bool = False
    messages: str = ''
    belong: int = 0
    btns: str = ''
    sp_btns: str = ''

    def __init__(self, *values):
        """button_id: int = 0\n
    text: str = ''\n
    admin_key: bool = False\n
    messages: str = ''\n
    belong: int = 0\n
    btns: str = ''\n
    sp_btns: str = ''"""

        try:
            self.person_id = values[0]
            if len(values) >= 2:
                self.button_text = values[1].decode('UTF-8') if type(values[1]) is bytes else values[1]
            if len(values) >= 3:
                self.button_admin_key = values[2]
            if len(values) >= 4:
                self.button_messages = json.loads(values[3]) if values[3] is not None else None
            if len(values) >= 5:
                self.button_belong_to = values[4]
            if len(values) >= 6:
                self.button_keyboards = json.loads(values[5]) if values[5] is not None else None
            if len(values) >= 7:
                self.button_special_keyboards = json.loads(values[6]) if values[6] is not None else None

        except IndexError as e:
            print('Person: ' + red(str(e)))
