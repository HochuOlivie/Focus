from . import keyboards
from aiogram import types
from utils import get_user
from aiogram.dispatcher import FSMContext


class Start:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp

    def register_commands(self):
        self.dp.register_message_handler(self.start, commands=["start"], state="*")

    def register_handlers(self):
        ...

    async def start(self, message: types.Message, state: FSMContext):
        user = get_user(message)
        async with state.proxy() as data:
            if user not in data:
                data[user] = {
                    "actions": [],
                    "categories": {},
                    "groups": {},
                    "set": {},
                    "log": {},
                    "stat": {},
                    "records": [],
                }

        msg = (
            "Hello! This is a bot for logging your daily activities. Bot helps:\n"
            "- analyse what your time is spent on\n"
            "- reduce time for useless activities\n"
            "- increase time for useful activities\n"
            "- become more productive\n"
            "- improve self-discipline"
        )
        await self.bot.send_message(
            message.from_user.id, msg, reply_markup=keyboards.kb_start
        )
