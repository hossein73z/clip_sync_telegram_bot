import json
from Functions.Coloring import red
from Objects.MyObject import MyObject


class Button(MyObject):
    def __init__(self,
                 id: int = 0,
                 text: str = '',
                 admin: int = 0,
                 messages: str = '',
                 belong: int = 0,
                 btns: str = '',
                 sp_btns: str = '',
                 values: tuple = ()):
        """
        Create a Button object.
        Named and default values are ignored if there is even one additional argument
        Use named arguments or pass the values in this order:

        :param id:
        :param text:
        :param admin:
        :param messages:
        :param belong:
        :param btns:
        :param sp_btns:
        :param values:
        """

        if len(values) > 0:
            try:
                self.id = values[0]
                if len(values) >= 2:
                    self.text = values[1].decode('UTF-8') if type(values[1]) is bytes else values[1]
                if len(values) >= 3:
                    self.admin = values[2]
                if len(values) >= 4:
                    self.messages = json.loads(values[3]) if values[3] else None
                if len(values) >= 5:
                    self.belong = values[4]
                if len(values) >= 6:
                    self.btns = json.loads(values[5]) if values[5] else None
                if len(values) >= 7:
                    self.sp_btns = json.loads(values[6]) if values[6] else None

            except IndexError as e:
                print('Button: ' + red(str(e)))

        else:
            self.id = id
            self.text = text
            self.admin = admin
            self.messages = messages
            self.belong = belong
            self.btns = btns
            self.sp_btns = sp_btns

