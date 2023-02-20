import json
from Functions.Coloring import red
from Objects.MyObject import MyObject


class Button(MyObject):
    def __init__(self, *values):
        """
        id: int = 0\n
        text: str = ''\n
        admin: int = 0\n
        messages: str = ''\n
        belong: int = 0\n
        btns: str = ''\n
        sp_btns: str = ''
        """

        try:
            self.id = values[0]
            if len(values) >= 2:
                self.text = values[1].decode('UTF-8') if type(values[1]) is bytes else values[1]
            if len(values) >= 3:
                self.admin = values[2]
            if len(values) >= 4:
                self.messages = json.loads(values[3]) if values[3] is not None else None
            if len(values) >= 5:
                self.belong = values[4]
            if len(values) >= 6:
                self.btns = json.loads(values[5]) if values[5] is not None else None
            if len(values) >= 7:
                self.sp_btns = json.loads(values[6]) if values[6] is not None else None

        except IndexError as e:
            print('Button: ' + red(str(e)))
