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
                 **kwargs):
        """
        Create a Person object.

        :param id:
        :param chat_id:
        :param first_name:
        :param last_name:
        :param username:
        :param progress:
        :param admin:
        :param btn_id:
        :param sp_btn_id:
        """

        self.id = id
        self.chat_id = chat_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.progress = json.loads(progress) if progress else None
        self.admin = admin
        self.btn_id = btn_id
        self.sp_btn_id = sp_btn_id

        for key in kwargs:
            setattr(self, key, kwargs[key])


class Button(MyObject):
    def __init__(self,
                 id: int = 0,
                 text: str = '',
                 admin: int = 0,
                 messages: str = '',
                 belong: int = 0,
                 btns: str = '',
                 sp_btns: str = '',
                 **kwargs):
        """
        Create a Button object.

        :param id:
        :param text:
        :param admin:
        :param messages:
        :param belong:
        :param btns:
        :param sp_btns:
        """

        self.id = id
        self.text = text
        self.admin = admin
        self.messages = messages
        self.belong = belong
        self.btns = json.loads(btns) if btns else None
        self.sp_btns = json.loads(sp_btns) if sp_btns else None

        for key in kwargs:
            setattr(self, key, kwargs[key])


class SPButton(MyObject):
    def __init__(self,
                 id: int = 0,
                 text: str = '',
                 admin: int = 0,
                 **kwargs):
        """
        Create a SPButton object.

        :param id:
        :param text:
        :param admin:
        """

        self.id = id
        self.text = text
        self.admin = admin

        for key in kwargs:
            setattr(self, key, kwargs[key])


class Setting(MyObject):
    def __init__(self,
                 id: int = 0,
                 name: str = '',
                 value=None,
                 **kwargs):
        """
        Create a Button object.

        :param id: Setting id
        :param name: Setting name
        :param value: Setting value
        """
        self.id = id
        self.name = name
        self.value = value

        for key in kwargs:
            setattr(self, key, kwargs[key])
