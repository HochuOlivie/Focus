from aiogram import types
from . import keyboards
from .state import States
from aiogram.dispatcher import FSMContext
from utils import get_user
from datetime import datetime, timedelta
from utils import week_days, get_hour_string


class Log:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp

    def register_commands(self):
        self.dp.register_message_handler(self._log, state="*", commands=["log"])

    def register_handlers(self):
        self.dp.register_message_handler(self._stop_recording, state=States.stop)

    async def _log(self, message: types.Message, state: FSMContext):
        user = get_user(message)
        msg = "Choose action🏄‍♂"
        async with state.proxy() as data:
            if len(message.text.split()) == 2:
                date = message.text.split()[1].strip()
                try:
                    datetime.strptime(date, "%d.%m")
                except:
                    await self.bot.send_message(
                        message.from_user.id,
                        'Enter correct date in format "day.month" (example: 12.06)',
                    )
                    return
                data[user]["log"]["date"] = date + f".{datetime.now().year}"
            else:
                data[user]["log"]["date"] = None
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
        print(123)
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
            date_str = data[user]["log"]["date"]
            if date_str is not None:
                date = datetime.strptime(data[user]["log"]["date"], "%d.%m.%Y")
            else:
                date = datetime.now()
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
                    "date": str(date),
                }
            )
            hours_string = get_hour_string(hours, 1, 1)
            msg = (
                f"✅ Record {action} {hours_string}"
                f' added ({week_days[date.weekday()]}, {date.strftime("%d.%m")})'
            )

            if category:
                points = int(category_points * total_seconds / 3600)
                msg += f'\n⬆{"⭐" * points} {points}p'
                del data[user]["log"]["category"]

        if date_str is None:
            kb = keyboards.get_log_more_action_keyboard()
        else:
            kb = keyboards.get_log_more_action_keyboard_double(date.strftime("%d.%m"))
        await self.bot.send_message(
            message.from_user.id, msg, reply_markup=kb,
        )
