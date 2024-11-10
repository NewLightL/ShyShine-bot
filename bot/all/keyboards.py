'''Keyboards for all'''

from aiogram.types import (
    InlineKeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import bot.all.lexicon_all as lex
import bot.client.lexicon_user as lex_user
from bot.db.user_req import User


remove = ReplyKeyboardRemove()

async def channel_board(my_channel: dict[str, dict[str, str]]) -> InlineKeyboardMarkup:
    """creates kb with channels name

    Parameters
    ----------
    my_channel : dict[str, dict[str, str]]

    Returns
    -------
    InlineKeyboardMarkup
        kb with channels name
    """
    channel = [
    InlineKeyboardButton(text='WILDBERRIES', url=my_channel['https']['wildberries']),
    InlineKeyboardButton(text='OZON', url=my_channel['https']['ozon']),
    InlineKeyboardButton(text='ALIEXPRESS', url=my_channel['https']['aliexpress']),
    InlineKeyboardButton(text='CATALOG', url='https://t.me/ShyShine_of_bot')
    ]
    build = InlineKeyboardBuilder()
    build.row(*channel, width=1)
    return build.as_markup()


async def start_board(my_channel: dict[str, dict[str, str]]) -> InlineKeyboardMarkup:
    """Creates a start keyboard

    Parameters
    ----------
    my_channel : dict[str, dict[str, str]]

    Returns
    -------
    InlineKeyboardMarkup
        kb for getting started with the bot
    """    
    build = InlineKeyboardBuilder()
    row_1 = [InlineKeyboardButton(text=channel.capitalize(), callback_data=channel)
             for channel in my_channel['@'].keys() if channel != 'pere']
    build.row(*row_1, width=3)
    build.add(InlineKeyboardButton(text='🔍Поиск приложения', callback_data='search'))
    build.add(InlineKeyboardButton(text=lex.TXT_EVERY_POST,
                                url=my_channel['https']['pere']))
    return build.adjust(3, 1, 1).as_markup()  # type: ignore


async def create_tegs_board(num_lst: int) -> InlineKeyboardMarkup:
    """Create peg table with tegs

    Parameters
    ----------
    num_lst : int
        _description_

    Returns
    -------
    InlineKeyboardMarkup
        

    Raises
    ------
    IndexError
        _description_
    """
    if num_lst < 0:
        raise IndexError('num_lst error')
    lst = await User.select_tegs_name_by_group()
    build = InlineKeyboardBuilder()
    build.row(*[InlineKeyboardButton(text=teg, callback_data=teg) for teg in lst[num_lst]], width=1)

    if num_lst == 0:  # first list
        build.row(InlineKeyboardButton(text=lex_user.peg_but['forward'],
                                       callback_data='forward'), width=1)

    if num_lst == len(lst) - 1:  # end list
        build.row(InlineKeyboardButton(text=lex_user.peg_but['back'],
                                       callback_data='back'), width=1)

    else:  # other list
        build.row(InlineKeyboardButton(text=lex_user.peg_but['back'],
                                       callback_data='back'),
                  InlineKeyboardButton(text=lex_user.peg_but['forward'],
                                       callback_data='forward'), width=2)

    build.add(InlineKeyboardButton(text=lex_user.peg_but['house'],
                                       callback_data='house'))
    return build.adjust(1, 1, 1,
                        1, 1, 1, 2, 1).as_markup()  # type: ignore


async def every_post(my_channel) -> InlineKeyboardMarkup:
    """kb with channel

    Parameters
    ----------
    my_channel : dict

    Returns
    -------
    InlineKeyboardMarkup
        kb with channel
    """    
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=lex.TXT_EVERY_POST,
                                url=my_channel['https']['pere']))
    return kb.as_markup()
