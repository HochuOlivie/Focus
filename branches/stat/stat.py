from aiogram import types
from . import keyboards
from .state import States
from aiogram.dispatcher import FSMContext
from utils import get_user
from datetime import datetime


class Stat:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp

    def register_commands(self):
        self.dp.register_message_handler(self._stat, state="*", commands=["stat"])

    def register_handlers(self):
        ...

    async def _stat(self, message: types.Message, state: FSMContext):
        user = get_user(message)
        async with state.proxy() as data:
            if not data[user]["records"]:
                await self.bot.send_message(
                    message.from_user.id,
                    "You have no stats to show. Try the /log command to log your activities.",
                )
            else:
                msg = "All actions🏄‍♂?"
                kb = keyboards.all_actions_fork()
                await self.bot.send_message(message.from_user.id, msg, reply_markup=kb)
