from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    stop = State()
    none = State()
