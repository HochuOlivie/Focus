from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from . import callback_consts as cbc


async def get_actions_keyboard(user, state):
    kb = InlineKeyboardMarkup()
    async with state.proxy() as data:
        for action in data[user]["actions"]:
            kb.add(
                InlineKeyboardButton(
                    action, callback_data=cbc.CHOOSE_TIME_ACTION + "_" + action
                )
            )
    return kb


def get_log_more_action_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Log one more action", callback_data=cbc.MORE_ACTION))
    return kb


def get_log_more_action_keyboard_double(date_str):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            f"Log one more action [{date_str}]", callback_data=cbc.MORE_ACTION_PAST
        )
    )
    kb.add(
        InlineKeyboardButton("Log one more action today", callback_data=cbc.MORE_ACTION)
    )
    return kb


def get_categories_keyboard(categories):
    kb = InlineKeyboardMarkup()
    for category, points in categories.items():
        kb.add(
            InlineKeyboardButton(
                f"{category} [{points}]",
                callback_data=cbc.CHOOSE_TIME_CATEGORY + "_" + category,
            )
        )
    return kb


def get_start_recording_fork():
    return (
        InlineKeyboardMarkup()
        .add(InlineKeyboardButton("Start recording", callback_data=cbc.START_RECORDING))
        .add(InlineKeyboardButton("Enter the time", callback_data=cbc.ENTER_TIME))
    )


def get_stop_recording_keyboard():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Stop", callback_data=cbc.STOP_RECORD)
    )
