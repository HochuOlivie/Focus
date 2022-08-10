from aiogram import types
from . import keyboards
from .state import States
from aiogram.dispatcher import FSMContext
from utils import get_user
from datetime import datetime, timedelta
from utils import week_days, truncate


class Log:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp
        self.dp.register_message_handler(self._stop_recording, state=States.stop)
        # self.dp.register_message_handler(self._get_group_action, state=States.add_group_state)

    def register_commands(self):
        self.dp.register_message_handler(self._log, state="*", commands=["log"])

    def register_handlers(self):
        self.dp.register_message_handler(self._stop_recording, state=States.stop)

    async def _log(self, message: types.Message, state: FSMContext):
        user = get_user(message)
        msg = "Choose action🏄‍♂"
        async with state.proxy() as data:
            if len(message.text.split()) == 2:
                data[user]["log"]["date"] = (
                    message.text.split()[1] + f".{datetime.now().year}"
                )
            else:
                data[user]["log"]["date"] = datetime.now().strftime("%d.%m.%Y")
            if data[user]["actions"]:
                await keyboards.get_actions_keyboard(user, state)
                await self.bot.send_message(
                    message.from_user.id,
                    msg,
                    reply_markup=await keyboards.get_actions_keyboard(user, state),
                )
            else:
                msg = "You need at least one action to log. Use /set command to set one"
                await self.bot.send_message(message.from_user.id, msg)

    async def _stop_recording(self, message: types.Message, state: FSMContext):
        try:
            hours = float(message.text.replace(",", "."))

        except:
            try:
                hours = (
                    int(message.text.split(":")[0])
                    + int(message.text.split(":")[1]) / 60
                )
            except:
                await self.bot.send_message(
                    message.from_user.id,
                    "Enter correct float number (example: 1,5) or hours:minutes",
                )
                return

        await States.none.set()

        async with state.proxy() as data:
            user = get_user(message)
            now = datetime.strptime(data[get_user(message)]["log"]["date"], "%d.%m.%Y")
            now.replace(year=datetime.now().year)
            total_seconds = hours * 3600
            action = data[user]["log"]["action"]
            category = (
                data[user]["log"]["category"]
                if "category" in data[user]["log"]
                else None
            )
            category_points = (
                int(data[user]["categories"][category]) if category else None
            )
            data[user]["records"].append(
                {
                    "duration": total_seconds,
                    "action": action,
                    "category_points": category_points,
                    "date": str(now),
                }
            )
            hours_str = truncate(hours, 1)
            if hours_str < 0.1:
                hours_str = "<0.1"
            hours_str = str(hours_str)
            msg = (
                f"✅ Record {action} {hours_str}h"
                f' added ({week_days[now.weekday()]}, {now.strftime("%d.%m")})'
            )

            if category:
                points = int(category_points * total_seconds / 3600)
                msg += f'\n⬆{"⭐" * points} {points}p'
                del data[user]["log"]["category"]
        await self.bot.send_message(
            message.from_user.id,
            msg,
            reply_markup=keyboards.get_log_more_action_keyboard(),
        )
