from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from . import callback_consts as cbc


def all_actions_fork():
    return (
        InlineKeyboardMarkup()
        .add(InlineKeyboardButton("All actions", callback_data=cbc.STAT_ALL_ACTIONS))
        .add(
            InlineKeyboardButton("Choose action", callback_data=cbc.STAT_CHOOSE_ACTION)
        )
    )


def get_actions_or_groups_keyboard(actions, groups):
    kb = InlineKeyboardMarkup()
    for action in actions:
        kb.add(
            InlineKeyboardButton(action, callback_data=cbc.STAT_ACTION + "_" + action)
        )
    for group in groups:
        kb.add(InlineKeyboardButton(group, callback_data=cbc.STAT_GROUP + "_" + group))
    return kb


def choose_interval_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("Today by actions", callback_data=cbc.TODAY_BY_ACTIONS)
    ).add(
        InlineKeyboardButton("Week by day", callback_data=cbc.WEEK_BY_DAY),
        InlineKeyboardButton("Week by actions", callback_data=cbc.WEEK_BY_ACTIONS),
    ).add(
        InlineKeyboardButton("Month by week", callback_data=cbc.MONTH_BY_WEEK),
        InlineKeyboardButton("Month by actions", callback_data=cbc.MONTH_BY_ACTIONS),
    ).add(
        InlineKeyboardButton("All time by week", callback_data=cbc.ALL_TIME_BY_WEEK),
        InlineKeyboardButton(
            "All time by actions", callback_data=cbc.ALL_TIME_BY_ACTIONS
        ),
    )
    return kb
