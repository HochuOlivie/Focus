from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    add_action_state = State()

    add_category_state = State()

    add_group_state = State()

    none = State()
