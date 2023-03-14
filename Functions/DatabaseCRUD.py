from Functions.Coloring import yellow, red, magenta, green
from MyObjects import engine, Base, factory
from MyObjects import Button, Message, SPButton, Setting
from sqlalchemy.orm import joinedload


def init():
    # Generate database schema
    Base.metadata.create_all(engine)

    # Create session
    session = factory()

    # Create objects list
    message1 = Message(id=1, text="Any text you type in here will be added to your pc clipboard.\n"
                                  "Use ((Back)) button to stop.")
    objects = [message1,
               Button(id=0, text='Main page', admin=0, btns=[[1]], sp_btns=[[2]]),
               Button(id=1, text='Send Text To PC 📤', admin=0, messages=[message1], belong=0, sp_btns=[[0]]),
               SPButton(id=0, text='🔙 Back 🔙', admin=0),
               SPButton(id=1, text='❌ Cancel ❌', admin=0),
               SPButton(id=2, text='Retrieve PC Clipboard 📋', admin=0),
               Setting(id=0, name='BOT_TOKEN')
               ]

    for item in objects:  # Add default values to tables
        try:
            session.add(item)
            session.commit()
        except Exception as e:
            print(f"init: {red(str(e))}")

    session.close()


def add(my_object: Base):
    session = factory()
    try:
        session.add(my_object)
        return True
    except Exception as e:
        print(f"add:  {yellow(str(my_object))}: {red(str(e))}")
        return False
    finally:
        session.commit()
        session.close()


def read(my_class: Base, **kwargs):
    session = factory()
    try:
        if my_class == Button:
            query = session.query(my_class).options(joinedload(my_class.messages))
        else:
            query = session.query(my_class)
        for key in kwargs:
            val = kwargs[key]
            if type(val) == set:
                query = query.filter(getattr(my_class, key).in_(val))
            else:
                query = query.filter(getattr(my_class, key) == val)

        result: list[my_class] = []
        for item in query.all():
            result.append(item)

        return result if result else None
    except Exception as e:
        print(f"read:  {yellow(str(my_class))}, {magenta(kwargs)}: {red(str(e))}")
        return None
    finally:
        session.close()


def edit(my_class: Base, id, **kwargs):
    session = factory()
    try:
        rec = session.query(my_class).filter(my_class.id == id)
        rec.update(kwargs)
        session.commit()
    except Exception as e:
        print(f"edit:  {yellow(str(my_class))}, {magenta(kwargs)}: {red(str(e))}")
    finally:
        session.close()
