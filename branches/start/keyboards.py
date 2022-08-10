from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from . import callback_consts as cbc


button_start = InlineKeyboardButton("Got it, let's move on", callback_data=cbc.START)
kb_start = InlineKeyboardMarkup().add(button_start)

button_add_actions = InlineKeyboardButton(
    "Add actions", callback_data=cbc.START_ADD_ACTION
)
kb_add_actions = InlineKeyboardMarkup().add(button_add_actions)
