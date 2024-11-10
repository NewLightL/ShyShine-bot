from typing import Any, Awaitable, Callable, Dict
from aiogram.fsm.middleware import BaseMiddleware  # type: ignore
from aiogram.types import Message, TelegramObject, User


class IsAdminMiddleware(BaseMiddleware):
    """Check user is admin"""
    async def __call__(self,
                       handler: Callable[[TelegramObject,
                                          Dict[str, Any]],
                                         Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        user: User = data.get('event_from_user')  # type: ignore

        if user.id not in data['admin_lst']:
            return
        return await handler(event, data)
