from Functions.Coloring import red
from Objects.MyObject import MyObject


class SPButton(MyObject):
    def __init__(self,
                 id: int = 0,
                 text: str = '',
                 admin: int = 0,
                 values: tuple = ()):
        """
        Create a Button object.
        Named and default values are ignored if there is even one additional argument
        Use named arguments or pass the values in this order:

        :param id:
        :param text:
        :param admin:
        :param values:
        """

        if len(values) > 0:
            try:
                self.id = values[0]
                if len(values) >= 2:
                    self.text = values[1].decode('UTF-8') if type(values[1]) is bytes else values[1]
                if len(values) >= 3:
                    self.admin = values[2]

            except IndexError as e:
                print('SPBButton: ' + red(str(e)))

        else:
            self.id = id
            self.text = text
            self.admin = admin
