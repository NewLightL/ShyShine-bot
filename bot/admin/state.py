'''State for admin'''

from aiogram.fsm.state import State, StatesGroup


class SendPost(StatesGroup):
    channel = State()
    media = State()
    name = State()
    desc = State()
    site = State()
    teg = State()
    repeat = State()


class SendPostPere(StatesGroup):
    y_n = State()
