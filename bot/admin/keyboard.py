"""Keyboard  for admin"""

from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import bot.all.lexicon_all as lex
from bot.db.admin_req import Admin


remove = ReplyKeyboardRemove()

yes_no = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text=lex.LEXICON['yes']),
    KeyboardButton(text=lex.LEXICON['no'])]  #& 1 row
], resize_keyboard=True)


async def create_kb(my_channel: dict[str, dict[str, str]]) -> ReplyKeyboardMarkup:
    """create reply kb with channels name

    Parameters
    ----------
    my_channel : dict[str, dict[str, str]]

    Returns
    -------
    ReplyKeyboardMarkup
        kb with channels name
    """    
    kb = ReplyKeyboardBuilder()
    button = [KeyboardButton(text=channel)
              for channel in my_channel['@'].keys()
              if channel != 'pere']
    kb.row(*button, width=2)
    return kb.as_markup()


async def create_kb_tegs() -> ReplyKeyboardMarkup:
    """create reply kb with tags name

    Returns
    -------
    ReplyKeyboardMarkup
        kb with tegs name
    """    
    kb = ReplyKeyboardBuilder()
    buttons = [KeyboardButton(text=f'#{teg}')
               for teg in await Admin.select_all_tegs()]
    kb.row(*buttons, width=2)
    return kb.as_markup()
