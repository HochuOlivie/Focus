from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from . import callback_consts as cbc
from . import keyboards
from .state import States
from utils import get_user
from datetime import datetime
from utils import week_days, get_datetime
from utils import truncate
from utils import get_user, get_hour_string, week_days


bot = None


async def choose_category(callback_query: types.CallbackQuery, state: FSMContext):
    msg = "Choose category🚦"
    user = get_user(callback_query)
    async with state.proxy() as data:
        data[user]["log"]["action"] = callback_query.data.split("_")[-1]
    async with state.proxy() as data:
        cats = data[user]["categories"]
        if not cats:
            await start_recording_fork(callback_query, state, True)
        else:
            await callback_query.message.edit_text(
                text=msg, reply_markup=keyboards.get_categories_keyboard(cats)
            )


async def start_recording_fork(
    callback_query: types.CallbackQuery, state: FSMContext, skip_category=False
):
    user = get_user(callback_query)

    if not skip_category:
        async with state.proxy() as data:
            data[user]["log"]["category"] = callback_query.data.split("_")[-1]

    async with state.proxy() as data:
        date_str = data[user]["log"]["date"]
        if date_str is not None:
            await enter_time(callback_query, state, skip_category)
            return

    msg = "Start recording or have you already performed the action?"
    kb = keyboards.get_start_recording_fork()
    await callback_query.message.edit_text(text=msg, reply_markup=kb)


async def enter_time(
    callback_query: types.CallbackQuery, state: FSMContext, skip_category=False
):
    await States.stop.set()
    msg = "Enter time🕝 in hh:mm or float hh format"
    await callback_query.message.edit_text(text=msg)


async def start_recording(
    callback_query: types.CallbackQuery, state: FSMContext, skip_category=False
):
    async with state.proxy() as data:
        user = get_user(callback_query)
        action = data[user]["log"]["action"]
        data[user]["log"]["start_recording"] = str(datetime.now())
        msg = f"Start recording {action}⏳"
    kb = keyboards.get_stop_recording_keyboard()
    await callback_query.message.edit_text(text=msg, reply_markup=kb)


async def stop_recording(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user = get_user(callback_query)
        date = get_datetime(data[user]["log"]["start_recording"])
        now = datetime.now()
        total_seconds = (now - date).total_seconds()
        hours = total_seconds / 3600
        hours_string = get_hour_string(hours, 1, 1)

        action = data[user]["log"]["action"]
        category = (
            data[user]["log"]["category"] if "category" in data[user]["log"] else None
        )
        category_points = int(data[user]["categories"][category]) if category else None
        data[user]["records"].append(
            {
                "date": str(date),
                "duration": total_seconds,
                "action": action,
                "category_points": category_points,
            }
        )
        msg = (
            f"✅ Record {action} {hours_string}"
            f' added ({week_days[date.weekday()]}, {now.strftime("%d.%m")})'
        )

        if category:
            points = int(category_points * total_seconds / 3600)
            msg += f'\n⬆{"⭐" * points} {points}p'
            del data[user]["log"]["category"]
    await callback_query.message.edit_text(
        text=msg, reply_markup=keyboards.get_log_more_action_keyboard()
    )


async def more_action(callback_query: types.CallbackQuery, state: FSMContext):
    user = get_user(callback_query)
    msg = "Choose action🏄‍♂"
    if callback_query.data == cbc.MORE_ACTION:
        async with state.proxy() as data:
            data[user]["log"]["date"] = None
    await keyboards.get_actions_keyboard(user, state)
    await callback_query.message.edit_text(text=callback_query.message.text)
    await bot.send_message(user, text=msg, reply_markup = await keyboards.get_actions_keyboard(user, state))


def register_callbacks(fbot, dp: Dispatcher):
    global bot
    bot = fbot
    dp.register_callback_query_handler(
        choose_category, lambda c: c.data.startswith(cbc.CHOOSE_TIME_ACTION), state="*"
    )
    dp.register_callback_query_handler(
        start_recording_fork,
        lambda c: c.data.startswith(cbc.CHOOSE_TIME_CATEGORY),
        state="*",
    )
    dp.register_callback_query_handler(enter_time, text=cbc.ENTER_TIME, state="*")
    dp.register_callback_query_handler(
        start_recording, text=cbc.START_RECORDING, state="*"
    )
    dp.register_callback_query_handler(stop_recording, text=cbc.STOP_RECORD, state="*")

    dp.register_callback_query_handler(more_action, text=cbc.MORE_ACTION, state="*")
    dp.register_callback_query_handler(
        more_action, text=cbc.MORE_ACTION_PAST, state="*"
    )
