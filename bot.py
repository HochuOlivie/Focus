from branches.branches import branches
from branches.callbacks import callbacks
from aiogram import executor


class ImsBot:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp
        branches_list = []
        for branch in branches:
            b = branch(self.bot, self.dp)
            branches_list.append(b)
            b.register_commands()
        for b in branches_list:
            b.register_handlers()
        for register_callback in callbacks:
            register_callback(self.bot, self.dp)

    def start(self):
        executor.start_polling(self.dp, skip_updates=True)
