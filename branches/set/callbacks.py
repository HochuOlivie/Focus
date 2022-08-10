from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from . import callback_consts as cbc
from . import keyboards
from .state import States
from utils import get_user


async def category_add(callback_query: types.CallbackQuery, state: FSMContext):
    await States.add_category_state.set()
    async with state.proxy() as data:
        user = get_user(callback_query)
        cats = data[user]["categories"]
        msg = ""
        if cats:
            if len(cats) == 1:
                msg += f"You have 1 category🚦: \n"
            else:
                msg += f"You already have {len(cats)} categories🚦: \n"
            for i in cats:
                msg += f"- {i} [{cats[i]}]\n"
            msg += "\n"
        msg += "Type name of new category🚦 of your activities"
        await callback_query.message.edit_text(text=msg)


async def category_add_end(callback_query: types.CallbackQuery, state: FSMContext):
    user = get_user(callback_query)
    async with state.proxy() as data:
        category = data[user]["set"]["category"]
        points = callback_query.data.split("_")[1]
        data[user]["categories"][category] = points
        categories = data[user]["categories"]
        if len(categories) == 1:
            msg = f"✅Ready! Now you have 1 category🚦️: \n"
        else:
            msg = f"✅Ready! Now you have {len(categories)} categories🚦️: \n"
        for category in categories:
            msg += f"- {category} [{categories[category]}]\n"
        await callback_query.message.edit_text(
            text=msg, reply_markup=keyboards.kb_add_cat_end
        )


async def action_add(callback_query: types.CallbackQuery, state: FSMContext):
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
        await callback_query.message.edit_text(text=msg)


async def group_add(callback_query: types.CallbackQuery, state: FSMContext):
    await States.add_group_state.set()
    async with state.proxy() as data:
        user = get_user(callback_query)
        groups = data[user]["groups"]
        msg = ""
        if groups:
            if len(groups) == 1:
                msg += f"You already have {len(groups)} group💼: \n"
            else:
                msg += f"You already have {len(groups)} groups💼: \n"
            for i in groups:
                msg += f'- {i} {" + ".join(groups[i])}\n\n'
        msg += "Type name of new group💼"
        await callback_query.message.edit_text(text=msg)


async def group_add_more_fork(callback_query: types.CallbackQuery, state: FSMContext):
    # TODO
    # await States.add_group_state.set()

    user = get_user(callback_query)
    new_action = callback_query.data.split("_")[-1]
    async with state.proxy() as data:
        group = data[user]["set"]["group"]
        if group not in data[user]["groups"]:
            data[user]["groups"][group] = [new_action]
        else:
            data[user]["groups"][group].append(new_action)
        full = all(
            action in data[user]["groups"][group] for action in data[user]["actions"]
        ) and len(data[user]["groups"][group]) == len(data[user]["actions"])

    msg = f"Action {new_action}🏄‍♂️ added to group {group}💼"
    kb = await keyboards.get_group_add_more(user, state, full)
    await callback_query.message.edit_text(text=msg, reply_markup=kb)


async def group_add_more(callback_query: types.CallbackQuery, state: FSMContext):
    user = get_user(callback_query)
    kb = await keyboards.get_actions_keyboard(user, state)
    async with state.proxy() as data:
        new_group = data[user]["set"]["group"]
    msg = f"Choose action🏄‍♂️ for Group💼 {new_group}"
    await callback_query.message.edit_text(text=msg, reply_markup=kb)


async def group_add_finish(callback_query: types.CallbackQuery, state: FSMContext):
    user = get_user(callback_query)
    async with state.proxy() as data:
        groups = data[user]["groups"]
        if len(groups) == 1:
            msg = f"✅Ready! Now you have 1 group💼:\n"
        else:
            msg = f"✅Ready! Now you have {len(groups)} groups💼:\n"
        for group in groups:
            msg += f'- {group}: {" + ".join(groups[group])}\n'
    await callback_query.message.edit_text(
        text=msg, reply_markup=keyboards.get_group_add_end()
    )


async def show_set(callback_query: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        user = get_user(callback_query)
        cats = data[user]["categories"]
        actions = data[user]["actions"]
        groups = data[user]["groups"]
        msg = ""

        if actions:
            if len(actions) == 1:
                msg += f"You have *{len(actions)} action🏄‍♂️*: \n"
            else:
                msg += f"You have *{len(actions)} actions🏄‍♂️*: \n"
            for i in actions:
                msg += f"- {i}\n"
            msg += "\n"
        if cats:
            if len(cats) == 1:
                msg += f"You have *{len(cats)} category🚦*: \n"
            else:
                msg += f"You have *{len(cats)} categories🚦*: \n"
            for i in cats:
                msg += f"- {i} \[{cats[i]}]\n"
            msg += "\n"
        if groups:
            if len(groups) == 1:
                msg += f"You have *{len(groups)} group💼*: \n"
            else:
                msg += f"You have *{len(groups)} groups💼*: \n"
            for i in groups:
                msg += f"- {i}: {' + '.join(data[user]['groups'][i])}\n"
            msg += "\n"
        await callback_query.message.edit_text(
            text=msg, reply_markup=keyboards.kb_set, parse_mode="Markdown"
        )


def register_callbacks(bot, dp: Dispatcher):
    dp.register_callback_query_handler(category_add, text=cbc.ADD_CAT, state="*")
    dp.register_callback_query_handler(
        category_add_end, lambda c: c.data.startswith(cbc.POINTS), state="*"
    )

    dp.register_callback_query_handler(action_add, text=cbc.ADD_ACTION, state="*")

    dp.register_callback_query_handler(group_add, text=cbc.ADD_GROUP, state="*")
    dp.register_callback_query_handler(
        group_add_more, text=cbc.CHOOSE_GROUP_ACTION, state="*"
    )
    dp.register_callback_query_handler(
        group_add_more_fork,
        lambda c: c.data.startswith(cbc.CHOOSE_GROUP_ACTION),
        state="*",
    )
    dp.register_callback_query_handler(
        group_add_finish, text=cbc.FINISH_GROUP_ADD, state="*"
    )

    dp.register_callback_query_handler(show_set, text=cbc.SHOW_SET, state="*")
