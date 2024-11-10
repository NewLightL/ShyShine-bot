'''Filter'''

from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import Message


class ChannelCorrect(BaseFilter):
    async def __call__(self, mess: Message,
                       my_channel: dict[str, dict[str, str]]) -> Any:
        return mess.text in my_channel['@'].keys()
