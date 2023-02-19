from Functions.Coloring import red
from Objects.MyObject import MyObject


class Person(MyObject):
    id: int = 0
    chat_id: int = 0
    first_name: str = None
    last_name: str = None
    username: str = None
    progress: str = None
    is_admin: bool = False
    btn_id: int = 0
    sp_btn_id: int = 0

    def __init__(self, *values):
        """id: int = 0\n
        chat_id: int = 0\n
        first_name: str = ''\n
        last_name: str = ''\n
        username: str = ''\n
        progress: str = ''\n
        is_admin: bool = False\n
        btn_id: int = 0\n
        sp_btn_id: int = 0"""

        try:
            self.id = values[0]
            if len(values) >= 2:
                self.chat_id = values[1]
            if len(values) >= 3:
                self.first_name = values[2].decode('UTF-8') if type(values[2]) is bytes else values[2]
            if len(values) >= 4:
                self.last_name = values[3].decode('UTF-8') if type(values[3]) is bytes else values[3]
            if len(values) >= 5:
                self.username = values[4].decode('UTF-8') if type(values[4]) is bytes else values[4]
            if len(values) >= 6:
                self.progress = values[5] if values[5] is not (None or "") else None
            if len(values) >= 7:
                self.is_admin = values[6]
            if len(values) >= 8:
                self.last_button_id = values[7]
            if len(values) >= 9:
                self.last_special_button_id = values[8]

        except IndexError as e:
            print('Person: ' + red(str(e)))
