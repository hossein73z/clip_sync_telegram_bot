import json

from Functions.Coloring import red


class MyObject:
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def float_to_string(value: float):
        text = str(value)
        texts = text.split('e')
        print(texts)
        if len(texts) < 2:
            return str(value)
        else:
            if int(texts[1]) < 0:
                result = '0.' + '0' * abs(int(texts[1]) + 1) + texts[0].replace('.', '')
            else:
                result = texts[0].replace('.', '') + '0' * abs(int(texts[1]))

            return result


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
        Create a Person object.
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


class SPButton(MyObject):
    def __init__(self,
                 id: int = 0,
                 text: str = '',
                 admin: int = 0,
                 values: tuple = ()):
        """
        Create a SPButton object.
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


class Setting(MyObject):
    def __init__(self,
                 id: int = 0,
                 name: str = '',
                 value=None,
                 values: tuple = ()):
        """
        Create a Button object.
        Named and default values are ignored if there is even one additional argument
        Use named arguments or pass the values in this order:

        :param id: Setting id
        :param name: Setting name
        :param value: Setting value
        :param values:
        """
        if len(values) > 0:
            try:
                self.id = values[0]
                if len(values) >= 2:
                    self.name = values[1].decode('UTF-8') if type(values[1]) is bytes else values[1]
                if len(values) >= 3:
                    self.value = values[2].decode('UTF-8') if type(values[2]) is bytes else values[2]

            except IndexError as e:
                print('Setting: ' + red(str(e)))

        else:
            self.id = id
            self.name = name
            self.value = value
