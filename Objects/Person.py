from Functions.Coloring import red
from Objects.MyObject import MyObject


class Person(MyObject):
    def __init__(self,
                 id: int = 0,
                 chat_id: int = 0,
                 first_name: str = '',
                 last_name: str = '',
                 username: str = '',
                 progress: str = '',
                 admin: int = 0,
                 btn_id: int = 0,
                 sp_btn_id: int = 0,
                 values: tuple = ()):
        """
        Create a Button object.
        Named and default values are ignored if there is even one additional argument
        Use named arguments or pass the values in this order:

        :param id:
        :param chat_id:
        :param first_name:
        :param last_name:
        :param username:
        :param progress:
        :param admin:
        :param btn_id:
        :param sp_btn_id:
        :param values:
        """

        if len(values) > 0:
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
                    self.progress = values[5] if values[5] else None
                if len(values) >= 7:
                    self.admin = values[6]
                if len(values) >= 8:
                    self.btn_id = values[7]
                if len(values) >= 9:
                    self.sp_btn_id = values[8]

            except IndexError as e:
                print('Person: ' + red(str(e)))

        else:
            self.id = id
            self.chat_id = chat_id
            self.first_name = first_name
            self.last_name = last_name
            self.username = username
            self.progress = progress
            self.admin = admin
            self.btn_id = btn_id
            self.sp_btn_id = sp_btn_id
