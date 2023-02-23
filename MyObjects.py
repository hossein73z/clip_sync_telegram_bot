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
    id: int
    chat_id: int
    first_name: str
    last_name: str
    username: str
    progress: str
    admin: int
    btn_id: int
    sp_btn_id: int

    def __init__(self, *args, **kwargs):
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

        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


class Button(MyObject):
    id: int
    text: str
    admin: int
    messages: str
    belong: int
    btns: str
    sp_btns: str

    def __init__(self, *args, **kwargs):
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
        for dictionary in args:
            for key in dictionary:
                if key in ['btns', 'sp_btns']:
                    dictionary[key] = json.loads(dictionary[key]) if dictionary[key] else None
                setattr(self, key, dictionary[key])
        for key in kwargs:
            if key in ['btns', 'sp_btns']:
                kwargs[key] = json.loads(kwargs[key]) if kwargs[key] else None
            setattr(self, key, kwargs[key])


class SPButton(MyObject):
    id: int
    text: str
    admin: int

    def __init__(self, *args, **kwargs):
        """
        Create a SPButton object.

        :param id:
        :param text:
        :param admin:
        """

        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])


class Setting(MyObject):
    id: int
    name: str
    value = None,

    def __init__(self, *args, **kwargs):
        """
        Create a Button object.

        :param id: Setting id
        :param name: Setting name
        :param value: Setting value
        """
        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
