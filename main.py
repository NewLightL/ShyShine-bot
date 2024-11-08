"""Main for bot"""

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

import bot.all.middleware as mid

from bot.client.user_handlers import router_user
from bot.admin.admin_handlers import router_admin
from bot.other.other_handlers import router_other
from bot.admin.middleware import IsAdminMiddleware
from bot.all.config import load_sett


async def main() -> None:
    """Main func"""
    conf = load_sett()

    bot = Bot(token=conf['bot_token'],  # type: ignore
          default=DefaultBotProperties(parse_mode=ParseMode.HTML,
                                       link_preview_is_disabled=True))

    dp = Dispatcher()

    dp['my_channel'] = conf['my_channel']  #? dictionary with channel names
    dp['admin_lst'] = conf['admin_lst']    #? list with id admins

    dp.include_routers(router_user, router_admin, router_other)

    dp.update.outer_middleware(mid.UserInChanel())
    router_admin.message.middleware(IsAdminMiddleware())

    await dp.start_polling(bot, allowed_updates=["message", "inline_query",
                                                 "chat_member", "callback_query"],
                           polling_timeout=20)


if __name__ == "__main__":
    asyncio.run(main())
