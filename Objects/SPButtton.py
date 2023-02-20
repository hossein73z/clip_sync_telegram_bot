from Functions.Coloring import red
from Objects.MyObject import MyObject


class SPButton(MyObject):
    id: int = 0
    text: str = ''
    admin_key: bool = False

    def __init__(self, *values):
        """
        id: int = 0\n
        text: str = ''\n
        admin_key: bool = False\n
        """

        try:
            self.id = values[0]
            if len(values) >= 2:
                self.text = values[1].decode('UTF-8') if type(values[1]) is bytes else values[1]
            if len(values) >= 3:
                self.admin_key = values[2]

        except IndexError as e:
            print('SPBButton: ' + red(str(e)))
