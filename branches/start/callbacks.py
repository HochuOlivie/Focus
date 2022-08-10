from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from . import callback_consts as cbc
from . import keyboards
from utils import get_user
from branches.set.state import States


bot = None


async def about(callback_query: types.CallbackQuery):
    msg1 = (
        "Hello! This is a bot for logging your daily activities. Bot helps:\n"
        "- analyse what your time is spent on\n"
        "- reduce time for useless activities\n"
        "- increase time for useful activities\n"
        "- become more productive\n"
        "- improve self-discipline"
    )
    msg = (
        "*About SET*\n"
        "For all type of settings you can use command /set\n\n"
        "First, you need to add the actions🏄‍♂️ you want to log. "
        "It can be work, sports, meditation. It is recommended to add from 3 to 10 categories.\n\n"
        "Second, you may add categories🚦 for your actions. "
        "For different categories you will receive different amount of points, which you earn while doing this category for one hour.\n\n"
        "Third, you can unite your actions in groups💼 to view stat not only by action, but also by group. "
        'For example, you can unite sport, therapy and meditation into a group "wellness" and check total hours for this group.\n\n'
        "*About LOG*\n"
        "To log an action use command /log\n\n"
        "*About STAT*\n"
        "Use /stat to show your statistics for the time lapse"
    )
    await callback_query.message.edit_text(text=msg1, parse_mode="Markdown")
    await bot.send_message(
        get_user(callback_query),
        text=msg,
        reply_markup=keyboards.kb_add_actions,
        parse_mode="Markdown",
    )


async def action_add(callback_query: types.CallbackQuery, state: FSMContext):
    msg1 = (
        "*About SET*\n"
        "For all type of settings you can use command /set\n\n"
        "First, you need to add the actions🏄‍♂️ you want to log. "
        "It can be work, sports, meditation. It is recommended to add from 3 to 10 categories.\n\n"
        "Second, you may add categories🚦 for your actions. "
        "For different categories you will receive different amount of points, which you earn while doing this category for one hour.\n\n"
        "Third, you can unite your actions in groups💼 to view stat not only by action, but also by group. "
        'For example, you can unite sport, therapy and meditation into a group "wellness" and check total hours for this group.\n\n'
        "*About LOG*\n"
        "To log an action use command /log\n\n"
        "*About STAT*\n"
        "Use /stat to show your statistics for the time lapse"
    )
    await States.add_action_state.set()
    async with state.proxy() as data:
        user = get_user(callback_query)
        actions = data[user]["actions"]
        msg = ""
        if actions:
            if len(actions) == 1:
                msg += f"You already have 1 action🏄‍♂: \n"
            else:
                msg += f"You already have {len(actions)} actions🏄‍♂: \n"
            for i in actions:
                msg += f"- {i}\n"
            msg += "\n"
        msg += "Type name of new action🏄‍♂️"
        await callback_query.message.edit_text(text=msg1)
        await bot.send_message(get_user(callback_query), msg)


def register_callbacks(fbot, dp: Dispatcher):
    global bot
    bot = fbot
    dp.register_callback_query_handler(about, text=cbc.START, state="*")
    dp.register_callback_query_handler(action_add, text=cbc.START_ADD_ACTION, state="*")
