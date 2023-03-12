from Functions.Coloring import yellow, red, magenta
from MyObjects import engine, Base, factory
from MyObjects import Button, SPButton, Setting


def init():
    # Generate database schema
    Base.metadata.create_all(engine)

    # Create session
    session = factory()

    try:
        # Add default values to tables
        session.add(Button(id=0, text='Main page', admin=0, btns=[[1]], sp_btns=[[2]]))
        session.add(Button(id=1, text='Send Text To PC 📤', admin=0, belong=0, sp_btns=[[0]]))

        session.add(SPButton(id=0, text='🔙 Back 🔙', admin=0))
        session.add(SPButton(id=1, text='❌ Cancel ❌', admin=0))
        session.add(SPButton(id=2, text='Retrieve PC Clipboard 📋', admin=0))

        session.add(Setting(id=0, name='BOT_TOKEN'))

        session.commit()
    except Exception as e:
        print(f"init: {red(str(e))}")
    finally:
        session.close()


def add(my_object: Base):
    session = factory()
    try:
        session.add(my_object)
    except Exception as e:
        print(f"add:  {yellow(str(my_object))}: {red(str(e))}")
    finally:
        session.commit()
        session.close()


def read(my_class: Base, **kwargs):
    session = factory()
    try:
        query = session.query(my_class)
        for key in kwargs:
            val = kwargs[key]
            if type(val) == set:
                query = query.filter(getattr(my_class, key).in_(val))
            else:
                query = query.filter(getattr(my_class, key) == val)

        result: list[my_class] = []
        for item in query:
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
