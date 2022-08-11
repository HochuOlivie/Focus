from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from . import callback_consts as cbc
from . import keyboards
from .state import States
from utils import get_user, get_hour_string
from datetime import datetime, timedelta
from . import bd
from utils import week_days, get_datetime
from math import floor


async def choose_action_or_group(
    callback_query: types.CallbackQuery, state: FSMContext
):
    msg = "Choose action or group"
    user = get_user(callback_query)
    async with state.proxy() as data:
        actions = data[user]["actions"]
        groups = data[user]["groups"]
        kb = keyboards.get_actions_or_groups_keyboard(actions, groups)
    await callback_query.message.edit_text(text=msg, reply_markup=kb)


async def choose_interval(callback_query: types.CallbackQuery, state: FSMContext):
    msg = "Choose interval"
    user = get_user(callback_query)
    async with state.proxy() as data:
        if callback_query.data.startswith(cbc.STAT_ACTION):
            data[user]["stat"]["type"] = "action"
        elif callback_query.data.startswith(cbc.STAT_GROUP):
            data[user]["stat"]["type"] = "group"
        elif callback_query.data.startswith(cbc.STAT_ALL_ACTIONS):
            data[user]["stat"]["type"] = "all_actions"
        data[user]["stat"]["value"] = callback_query.data.split("_")[-1]

    kb = keyboards.choose_interval_keyboard()
    await callback_query.message.edit_text(text=msg, reply_markup=kb)


async def today_by_actions(callback_query: types.CallbackQuery, state: FSMContext):
    user = get_user(callback_query)
    date = datetime.now().date()
    async with state.proxy() as data:
        user_has_cats = bool(data[user]["categories"])
        if data[user]["stat"]["type"] == "action":
            action = data[user]["stat"]["value"]
            res = bd.agregate_actions_by_date(user, data, [action], date, date)

        elif data[user]["stat"]["type"] == "group":
            group = data[user]["stat"]["value"]
            res = bd.agregate_actions_by_group(user, data, group, date, date)

        elif data[user]["stat"]["type"] == "all_actions":
            actions = data[user]["actions"]
            res = bd.agregate_actions_by_date(user, data, actions, date, date)

        msg = ""
        actions_stat = res["actions"]
        for action in actions_stat:
            hours = actions_stat[action]["hours"]
            if hours > 0:
                hours_str = get_hour_string(hours, 1, 1)
                msg += f"{action} {hours_str}"
                points = actions_stat[action]["points"]
                if user_has_cats:
                    msg += f" / {floor(points)}p"
                msg += "\n"
        msg += "Total:\n"
        if user_has_cats:
            msg += f"{'⭐' * floor(res['total_points'] // 5) + ' '}{get_hour_string(res['total_hours'], 1, 1)} / {floor(res['total_points'])}p\n"
            msg += f"*1 star for each 5 points"
        else:
            msg += f"{get_hour_string(res['total_hours'], 1, 1)}"
        await callback_query.message.edit_text(text=msg)


async def week_by_actions(callback_query: types.CallbackQuery, state: FSMContext):
    user = get_user(callback_query)
    date_to = datetime.now().date()
    date_from = date_to - timedelta(days=7)

    async with state.proxy() as data:
        user_has_cats = bool(data[user]["categories"])
        if data[user]["stat"]["type"] == "action":
            action = data[user]["stat"]["value"]
            res = bd.agregate_actions_by_date(user, data, [action], date_from, date_to)
        elif data[user]["stat"]["type"] == "group":
            group = data[user]["stat"]["value"]
            res = bd.agregate_actions_by_group(user, data, group, date_from, date_to)
        elif data[user]["stat"]["type"] == "all_actions":
            actions = data[user]["actions"]
            res = bd.agregate_actions_by_date(user, data, actions, date_from, date_to)

        msg = f'{date_from.strftime("%d.%m")} - {date_to.strftime("%d.%m")}\n'
        actions_stat = res["actions"]

        for action in actions_stat:
            hours = actions_stat[action]["hours"]
            if hours > 0:
                hours_str = get_hour_string(hours, 1, 0)
                msg += f"{action} {hours_str}"
                points = actions_stat[action]["points"]
                if user_has_cats:
                    msg += f" / {floor(points)}p"
                msg += "\n"
        msg += "Total:\n"
        if user_has_cats:
            msg += f"{get_hour_string(res['total_hours'], 1, 0)} / {floor(res['total_points'])}p\n"
        else:
            msg += f"{get_hour_string(res['total_hours'], 1, 0)}"
        await callback_query.message.edit_text(text=msg)


async def month_by_actions(callback_query: types.CallbackQuery, state: FSMContext):
    user = get_user(callback_query)
    date_to = datetime.now().date()
    date_from = date_to.replace(day=1)

    async with state.proxy() as data:
        user_has_cats = bool(data[user]["categories"])
        if data[user]["stat"]["type"] == "action":
            action = data[user]["stat"]["value"]
            res = bd.agregate_actions_by_date(user, data, [action], date_from, date_to)
        elif data[user]["stat"]["type"] == "group":
            group = data[user]["stat"]["value"]
            res = bd.agregate_actions_by_group(user, data, group, date_from, date_to)
        elif data[user]["stat"]["type"] == "all_actions":
            actions = data[user]["actions"]
            res = bd.agregate_actions_by_date(user, data, actions, date_from, date_to)

        msg = f'{date_from.strftime("%d.%m")} - {date_to.strftime("%d.%m")}\n'
        actions_stat = res["actions"]

        for action in actions_stat:
            hours = actions_stat[action]["hours"]
            if hours > 0:
                hours_str = get_hour_string(hours, 0, 0)
                msg += f"{action} {hours_str}"
                points = actions_stat[action]["points"]
                if user_has_cats:
                    msg += f" / {floor(points)}p"
                msg += "\n"
        msg += "Total:\n"
        if user_has_cats:
            msg += f"{get_hour_string(res['total_hours'], 0, 0)} / {floor(res['total_points'])}p\n"
        else:
            msg += f"{get_hour_string(res['total_hours'], 0, 0)}"
        await callback_query.message.edit_text(text=msg)


async def all_time_by_actions(callback_query: types.CallbackQuery, state: FSMContext):
    user = get_user(callback_query)
    date_to = datetime.now().date()
    async with state.proxy() as data:
        date_from = get_datetime(
            min(data[user]["records"], key=lambda x: get_datetime(x["date"])).get(
                "date"
            )
        ).date()

    async with state.proxy() as data:
        user_has_cats = bool(data[user]["categories"])
        if data[user]["stat"]["type"] == "action":
            action = data[user]["stat"]["value"]
            res = bd.agregate_actions_by_date(user, data, [action], date_from, date_to)
        elif data[user]["stat"]["type"] == "group":
            group = data[user]["stat"]["value"]
            res = bd.agregate_actions_by_group(user, data, group, date_from, date_to)
        elif data[user]["stat"]["type"] == "all_actions":
            actions = data[user]["actions"]
            res = bd.agregate_actions_by_date(user, data, actions, date_from, date_to)

        msg = f'{date_from.strftime("%d.%m")} - {date_to.strftime("%d.%m")}\n'
        actions_stat = res["actions"]

        for action in actions_stat:
            hours = actions_stat[action]["hours"]
            if hours > 0:
                hours_str = get_hour_string(hours, 0, 0)
                msg += f"{action} {hours_str}"
                points = actions_stat[action]["points"]
                if user_has_cats:
                    msg += f" / {floor(points)}p"
                msg += "\n"
        msg += "Total:\n"
        if user_has_cats:
            msg += f"{get_hour_string(res['total_hours'], 0, 0)} / {floor(res['total_points'])}p\n"
        else:
            msg += f"{get_hour_string(res['total_hours'], 0, 0)}"
        await callback_query.message.edit_text(text=msg)


async def week_by_day(callback_query: types.CallbackQuery, state: FSMContext):
    user = get_user(callback_query)
    date_to = datetime.now().date()
    date_from = date_to - timedelta(days=7)

    async with state.proxy() as data:
        user_has_cats = bool(data[user]["categories"])
        if data[user]["stat"]["type"] == "action":
            action = data[user]["stat"]["value"]
            res = bd.agregate_days_by_week(user, data, [action], date_from, date_to)
        elif data[user]["stat"]["type"] == "group":
            group = data[user]["stat"]["value"]
            res = bd.agregate_days_by_week(
                user, data, data[user]["groups"][group], date_from, date_to
            )
        elif data[user]["stat"]["type"] == "all_actions":
            actions = data[user]["actions"]
            res = bd.agregate_days_by_week(user, data, actions, date_from, date_to)
    msg = f'{date_from.strftime("%d.%m")} {week_days[date_from.weekday()]} - {date_to.strftime("%d.%m")} {week_days[date_to.weekday()]}\n'
    for i in res["days"]:
        hours = res["days"][i]["hours"]
        hours_str = get_hour_string(hours, 1, 0)
        s = f"{hours_str}"
        points = res["days"][i]["points"]
        if user_has_cats:
            s = "⭐" * floor(points // 5) + s + f" / {floor(points)}p"
        msg += f"{s}\n"
    if user_has_cats:
        msg += "*1 star for each 5 points\n"
    await callback_query.message.edit_text(text=msg)


async def month_by_week(callback_query: types.CallbackQuery, state: FSMContext):
    user = get_user(callback_query)
    date_to = datetime.now().date()
    date_from = date_to - timedelta(days=date_to.weekday(), weeks=4)
    total_weeks = 5

    async with state.proxy() as data:
        user_has_cats = bool(data[user]["categories"])
        if data[user]["stat"]["type"] == "action":
            action = data[user]["stat"]["value"]
            res = bd.agregate_weeks_by_month(user, data, [action], date_from, date_to)
        elif data[user]["stat"]["type"] == "group":
            group = data[user]["stat"]["value"]
            res = bd.agregate_weeks_by_month(
                user, data, data[user]["groups"][group], date_from, date_to
            )
        elif data[user]["stat"]["type"] == "all_actions":
            actions = data[user]["actions"]
            res = bd.agregate_weeks_by_month(user, data, actions, date_from, date_to)
    msg = (
        ", ".join(
            [
                (date_from + timedelta(days=i * 7)).strftime("%d.%m")
                for i in range(total_weeks)
            ]
        )
        + "\n"
    )
    for i in res["weeks"]:
        hours = res["weeks"][i]["hours"]
        hours_str = get_hour_string(hours, 0, 0)
        s = f"{hours_str}"
        points = res["weeks"][i]["points"]
        if user_has_cats:
            s = "⭐" * floor(points // 20) + s + f" / {floor(points)}p"
        msg += s + "\n"
    if user_has_cats:
        msg += "*1 star for each 20 points\n"
    await callback_query.message.edit_text(text=msg)


async def all_time_by_week(callback_query: types.CallbackQuery, state: FSMContext):
    user = get_user(callback_query)
    date_to = datetime.now().date()
    async with state.proxy() as data:
        date_from = get_datetime(
            min(data[user]["records"], key=lambda x: get_datetime(x["date"])).get(
                "date"
            )
        ).date()
        date_from = date_from - timedelta(days=date_from.weekday())
    total_weeks = (date_to - date_from).days // 7 + 1

    async with state.proxy() as data:
        user_has_cats = bool(data[user]["categories"])
        if data[user]["stat"]["type"] == "action":
            action = data[user]["stat"]["value"]
            res = bd.agregate_weeks_by_month(user, data, [action], date_from, date_to)
        elif data[user]["stat"]["type"] == "group":
            group = data[user]["stat"]["value"]
            res = bd.agregate_weeks_by_month(
                user, data, data[user]["groups"][group], date_from, date_to
            )
        elif data[user]["stat"]["type"] == "all_actions":
            actions = data[user]["actions"]
            res = bd.agregate_weeks_by_month(user, data, actions, date_from, date_to)
    msg = f'{total_weeks} weeks, {date_from.strftime("%d.%m")} - {date_to.strftime("%d.%m")}\n'
    for i in res["weeks"]:
        hours = res["weeks"][i]["hours"]
        hours_str = get_hour_string(hours, 0, 0)
        s = f"{hours_str}"
        points = res["weeks"][i]["points"]
        if user_has_cats:
            s = "⭐" * floor(points // 20) + s + f" / {floor(points)}p"
        msg += s + "\n"
    if user_has_cats:
        msg += "*1 star for each 20 points\n"
    await callback_query.message.edit_text(text=msg)


def register_callbacks(bot, dp: Dispatcher):
    dp.register_callback_query_handler(
        choose_action_or_group, text=cbc.STAT_CHOOSE_ACTION, state="*"
    )
    dp.register_callback_query_handler(
        choose_interval,
        lambda c: c.data.startswith(cbc.STAT_ACTION)
        or c.data.startswith(cbc.STAT_GROUP)
        or c.data.startswith(cbc.STAT_ALL_ACTIONS),
        state="*",
    )
    dp.register_callback_query_handler(
        today_by_actions, text=cbc.TODAY_BY_ACTIONS, state="*"
    )
    dp.register_callback_query_handler(
        week_by_actions, text=cbc.WEEK_BY_ACTIONS, state="*"
    )
    dp.register_callback_query_handler(
        month_by_actions, text=cbc.MONTH_BY_ACTIONS, state="*"
    )
    dp.register_callback_query_handler(
        all_time_by_actions, text=cbc.ALL_TIME_BY_ACTIONS, state="*"
    )

    dp.register_callback_query_handler(week_by_day, text=cbc.WEEK_BY_DAY, state="*")
    dp.register_callback_query_handler(month_by_week, text=cbc.MONTH_BY_WEEK, state="*")
    dp.register_callback_query_handler(
        all_time_by_week, text=cbc.ALL_TIME_BY_WEEK, state="*"
    )
