''''Middleware'''

from typing import Any, Awaitable, Callable, Dict
from aiogram.fsm.middleware import BaseMiddleware  # type: ignore
from aiogram.types import TelegramObject, User, ChatMemberLeft

import bot.all.keyboards as kb


class UserInChanel(BaseMiddleware):
    """Checks if the user is in the channels"""
    async def __call__(self,
                       handler: Callable[[TelegramObject,
                                          Dict[str, Any]],
                                         Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        user: User = data.get('event_from_user')  # type: ignore
        my_channel: dict[str, dict[str, str]] = data['my_channel']
        lst = [await event.bot.get_chat_member(channel, user.id)  # type: ignore
                for channel in my_channel['@'].values()
                if channel != '@ShyShine_pere']
        new = [not isinstance(typ, ChatMemberLeft) for typ in lst]

        if any(new):
            await handler(event, data)
            return

        await event.bot.send_message(user.id,  # type: ignore
                                     'Ты не подписан на наши каналы\n'\
                                     'Для продолжения подпишись на любой по кнопкам снизу\n'\
                                     "После снова нажми на любую команду",
                                    reply_markup=await kb.channel_board(my_channel))
        return
