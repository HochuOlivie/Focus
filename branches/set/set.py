from aiogram import types
from . import keyboards
from .state import States
from aiogram.dispatcher import FSMContext
from utils import get_user


class Set:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp

    def register_commands(self):
        self.dp.register_message_handler(self._set, state="*", commands=["set"])

    def register_handlers(self):
        self.dp.register_message_handler(
            self._add_points, state=States.add_category_state
        )
        self.dp.register_message_handler(
            self._add_action, state=States.add_action_state
        )
        self.dp.register_message_handler(
            self._get_group_action, state=States.add_group_state
        )

    async def _set(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            user = get_user(message)
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
            if any([cats, actions, groups]):
                await self.bot.send_message(
                    message.from_user.id,
                    text=msg,
                    reply_markup=keyboards.kb_set,
                    parse_mode="Markdown",
                )
            else:
                msg = "You have no categories, actions or groups"
                await self.bot.send_message(
                    message.from_user.id,
                    text=msg,
                    reply_markup=keyboards.kb_set,
                    parse_mode="Markdown",
                )

    async def _add_points(self, message: types.Message, state: FSMContext):
        await States.none.set()
        category = message.text
        user = get_user(message)
        async with state.proxy() as data:
            data[user]["set"]["category"] = category
        msg = "Add points per hour for doing this category🚦"
        await self.bot.send_message(
            message.from_user.id, msg, reply_markup=keyboards.kb_points
        )

    async def _add_action(self, message: types.Message, state: FSMContext):
        await States.none.set()
        new_action = message.text
        user = get_user(message)
        async with state.proxy() as data:
            actions = data[user]["actions"]
            actions.append(new_action)
            if len(actions) == 1:
                msg = f"✅Ready! Now you have 1 action🏄‍♂️: \n"
            else:
                msg = f"✅Ready! Now you have {len(actions)} actions🏄‍♂️: \n"
            for action in actions:
                msg += f"- {action}\n"
            await self.bot.send_message(
                message.from_user.id, msg, reply_markup=keyboards.kb_add_action
            )

    async def _add_action_show(self, message: types.Message, state: FSMContext):
        await States.none.set()
        user = get_user(message)
        async with state.proxy() as data:
            actions = data[user]["actions"]
            if len(actions) == 1:
                msg = f"✅Ready! Now you have 1 action🏄‍♂️: \n"
            else:
                msg = f"✅Ready! Now you have {len(actions)} actions🏄‍♂️: \n"
            for action in actions:
                msg += f"- {action}\n"
            await self.bot.send_message(
                message.from_user.id, msg, reply_markup=keyboards.kb_add_action
            )

    async def _get_group_action(self, message: types.Message, state: FSMContext):
        await States.none.set()
        user = get_user(message)
        async with state.proxy() as data:
            data[user]["set"]["group"] = message.text
        kb = await keyboards.get_actions_keyboard(user, state)
        async with state.proxy() as data:
            new_group = data[user]["set"]["group"]
        msg = f"Choose action🏄‍♂️ for Group💼 {new_group}"
        await self.bot.send_message(message.from_user.id, msg, reply_markup=kb)
