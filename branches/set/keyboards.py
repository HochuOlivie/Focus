from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from . import callback_consts as cbc


inline_keyboard = []
for i in range(0, 5, 2):
    if i == 4:
        inline_keyboard.append(
            [InlineKeyboardButton(str(i), callback_data=cbc.POINTS + "_" + str(i))]
        )
        break
    inline_keyboard.append(
        [
            InlineKeyboardButton(str(i), callback_data=cbc.POINTS + "_" + str(i)),
            InlineKeyboardButton(
                str(i + 1), callback_data=cbc.POINTS + "_" + str(i + 1)
            ),
        ]
    )
kb_points = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


button_add_cat_end1 = InlineKeyboardButton(
    "Add one more category🚦", callback_data=cbc.ADD_CAT
)
button_show_all_set = InlineKeyboardButton(
    "Show all my set", callback_data=cbc.SHOW_SET
)
kb_add_cat_end = (
    InlineKeyboardMarkup().add(button_add_cat_end1).add(button_show_all_set)
)


kb_add_action = (
    InlineKeyboardMarkup()
    .add(InlineKeyboardButton("Add one more action🏄‍♂️", callback_data=cbc.ADD_ACTION))
    .add(InlineKeyboardButton("Show all my set", callback_data=cbc.SHOW_SET))
)

kb_set = (
    InlineKeyboardMarkup()
    .add(InlineKeyboardButton("Add action🏄‍♂️", callback_data=cbc.ADD_ACTION))
    .add(InlineKeyboardButton("Add category🚦", callback_data=cbc.ADD_CAT),)
    .add(InlineKeyboardButton("Add group💼", callback_data=cbc.ADD_GROUP))
)


async def get_actions_keyboard(user, state):
    kb = InlineKeyboardMarkup()
    async with state.proxy() as data:
        new_group = data[user]["set"]["group"]
        # excluding existing actions
        if new_group not in data[user]["groups"]:
            for action in data[user]["actions"]:
                kb.add(
                    InlineKeyboardButton(
                        action, callback_data=cbc.CHOOSE_GROUP_ACTION + "_" + action
                    )
                )
        else:
            for action in data[user]["actions"]:
                if action not in data[user]["groups"][new_group]:
                    kb.add(
                        InlineKeyboardButton(
                            action, callback_data=cbc.CHOOSE_GROUP_ACTION + "_" + action
                        )
                    )
    return kb


async def get_group_add_more(user, state, full=False):
    kb = InlineKeyboardMarkup()
    async with state.proxy() as data:
        if not full:
            kb.add(
                InlineKeyboardButton(
                    f'Add one more action to group {data[user]["set"]["group"]}',
                    callback_data=cbc.CHOOSE_GROUP_ACTION,
                )
            )
        kb.add(
            InlineKeyboardButton(
                f'Finish adding actions to group {data[user]["set"]["group"]}',
                callback_data=cbc.FINISH_GROUP_ADD,
            )
        )
    return kb


def get_group_add_end():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("Add one more group💼", callback_data=cbc.ADD_GROUP)
    ).add(InlineKeyboardButton("Show all my set", callback_data=cbc.SHOW_SET))
    return kb
