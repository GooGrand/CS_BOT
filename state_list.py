from aiogram.fsm.state import State, StatesGroup


class reserve_form(StatesGroup):
    name = State()
    surname = State()
    phone = State()
    amount = State()
    date = State()
    time = State()
    comment = State()
    confirm = State()


class item(StatesGroup):
    discounters = State()
    apply = State()
    payment = State()
    comment = State()


class expenses(StatesGroup):
    apply = State()
    amount = State()
    comment = State()
