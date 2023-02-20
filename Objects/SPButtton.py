from Functions.Coloring import red
from Objects.MyObject import MyObject


class SPButton(MyObject):
    def __init__(self, *values):
        """
        id: int = 0\n
        text: str = ''\n
        admin: int = 0\n
        """

        try:
            self.id = values[0]
            if len(values) >= 2:
                self.text = values[1].decode('UTF-8') if type(values[1]) is bytes else values[1]
            if len(values) >= 3:
                self.admin = values[2]

        except IndexError as e:
            print('SPBButton: ' + red(str(e)))
