'''Filter'''

from typing import Any

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

from bot.db.user_req import User


class CorrectChannels(BaseFilter):
    async def __call__(self, call: CallbackQuery) -> Any:
        channels_lst = await User.select_channels_name()
        return call.data in channels_lst


class CorrectTegs(BaseFilter):
    async def __call__(self, call: CallbackQuery) -> Any:
        tegs_lst = await User.select_tegs_name()
        return call.data in tegs_lst


class CorrectItems(BaseFilter):
    async def __call__(self, call: CallbackQuery) -> Any:
        lst = await User.select_items_all()
        return call.data in lst
