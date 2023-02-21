import sqlite3
from Functions.Coloring import red, green, bright, cyan, yellow
from Objects import MyObject
from Objects.Buttton import Button
from Objects.SPButtton import SPButton

PERSONS_TABLE = 'persons'
BUTTONS_TABLE = 'raw_btns'
SP_BUTTONS_TABLE = 'raw_sp_btns'
SETTINGS_TABLE = 'settings'


def init():
    # Create tables
    create_table(PERSONS_TABLE)
    create_table(BUTTONS_TABLE)
    create_table(SP_BUTTONS_TABLE)
    create_table(SETTINGS_TABLE)

    # Add default values to tables
    buttons = [
        Button(id=0, text='Main page', admin=0, btns="[[1],[2]]"),
        Button(id=1, text='Button 2', admin=0, belong=0, sp_btns="[[0]]"),
        Button(id=2, text='Button 3', admin=0, belong=0, btns="[[3]]", sp_btns="[[0]]"),
        Button(id=3, text='Button 4', admin=0, belong=2, sp_btns="[[0]]")
    ]
    sp_buttons = [
        SPButton(id=0, text='🔙 Back 🔙', admin=0)
    ]

    for button in buttons:
        add(BUTTONS_TABLE, button)
    for sp_button in sp_buttons:
        add(SP_BUTTONS_TABLE, sp_button)


def connect():
    return sqlite3.connect('./database.db')


def create_table(*table_names: str):
    connection = connect()
    cursor = connection.cursor()

    for table_name in table_names:
        print(f'create_table: Creating table {bright(table_name)}')

        try:
            if table_name == PERSONS_TABLE:
                cursor.execute(f"""CREATE TABLE IF NOT EXISTS {PERSONS_TABLE} (
                        id INTEGER PRIMARY KEY,
                        chat_id LONG NOT NULL UNIQUE DEFAULT 0,
                        first_name TEXT NOT NULL,
                        last_name TEXT,
                        username TEXT,
                        progress TEXT,
                        admin int NOT NULL DEFAULT 0,
                        btn_id INT NOT NULL DEFAULT 0,
                        sp_btn_id INT
                        ) """)
            elif table_name == BUTTONS_TABLE:
                cursor.execute(f"""CREATE TABLE IF NOT EXISTS {BUTTONS_TABLE} (
                        id INTEGER PRIMARY KEY,
                        text TEXT NOT NULL,
                        admin int NOT NULL DEFAULT 0,
                        messages TEXT,
                        belong INT,
                        btns TEXT,
                        sp_btns TEXT
                        ) """)
            elif table_name == SP_BUTTONS_TABLE:
                cursor.execute(f"""CREATE TABLE IF NOT EXISTS {SP_BUTTONS_TABLE} (
                        id INTEGER PRIMARY KEY,
                        text TEXT NOT NULL,
                        admin int NOT NULL DEFAULT 0
                        ) """)
            elif table_name == SETTINGS_TABLE:
                cursor.execute(f"""CREATE TABLE IF NOT EXISTS {SETTINGS_TABLE} (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        value text NOT NULL DEFAULT ''
                        ) """)

            connection.commit()
            print('create_table: ' + green(f'Table {bright(table_name)} created'))

        except sqlite3.OperationalError as e:
            print('create_table: ' + red(str(e)))

        finally:
            cursor.close()
            connection.close()


def add(table: str, my_object: MyObject):
    print(f'add: {yellow(table)} | Adding new item to {bright(table)} table')

    pairs = my_object.__dict__
    pairs = {key: val for key, val in pairs.items() if val is not None}
    keys_str = ', '.join(pairs.keys())
    vals_str = ', '.join(map(lambda s: f"'{s}'" if type(s) == str or list else s, pairs.values()))
    sql = f"INSERT INTO {table} ({keys_str}) VALUES ({vals_str})"

    print('add: ' + cyan('Completed sql query: ') + sql)
    connection = connect()
    cursor = connection.cursor()
    try:
        result = cursor.execute(sql)
        connection.commit()
        print(f'add: {yellow(table)} | {green(f"New item added to {bright(table)} table")}')

        return result
    except sqlite3.IntegrityError as e:
        print('add_person: ' + red(str(e)))
        return None
    finally:
        cursor.close()
        connection.close()


def read(table: str, my_object: MyObject, **kwargs):
    # Create sql query
    sql = f"SELECT * FROM {table}"

    condition = ''
    if len(kwargs):
        # Managing 'WHERE' statement
        sql += ' WHERE '
        condition = ' AND '.join(
            ' = '.join((key, "'" + str(val) + "'")) for key, val in kwargs.items())

    sql += condition
    print('read: ' + yellow(table) + ' | ' + cyan('Completed sql query: ') + sql)

    # Reading database
    connection = connect()
    curses = connection.cursor()

    try:
        fetched = curses.execute(sql).fetchall()

        items: list[MyObject] = []
        for temp in fetched:
            print(str(type(temp))+': '+str(temp))
            item = my_object(values=temp)
            items.append(item)

        return items if items else None

    except sqlite3.OperationalError as e:
        print(red(str(e)))
        return None

    finally:
        curses.close()
        connection.close()


def edit(table: str, **kwargs):
    # Create sql query
    sql = f"UPDATE {table}"
    id = kwargs.pop('id')
    condition = ''
    if len(kwargs):
        # Managing 'WHERE' statement
        sql += ' SET '
        condition = ', '.join(
            ' = '.join((key, "'" + str(val) + "'")) for key, val in kwargs.items())

    sql += condition + f" WHERE id = {id}"
    print('edit: ' + yellow(table) + ' | ' + cyan('Completed sql query: ') + sql)

    # Reading database
    connection = connect()
    curses = connection.cursor()

    try:
        fetched = curses.execute(sql).fetchall()
        connection.commit()

        return fetched if not None else None

    except sqlite3.OperationalError as e:
        print(red(str(e)))
        return None

    finally:
        curses.close()
        connection.close()
