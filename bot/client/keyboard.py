'''Keyboard for user'''

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

import bot.client.lexicon_user as lex_us
from bot.db.user_req import User


return_home = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=lex_us.peg_but['house'],
                          callback_data='house')]
])

async def create_peg_kb_tegs(num_lst: int) -> InlineKeyboardMarkup:
    """Create peg table tegs

    Parameters
    ----------
    num_lst : int
        _description_

    Returns
    -------
    InlineKeyboardMarkup
        _description_

    Raises
    ------
    IndexError
        _description_
    """    
    if num_lst < 0:
        raise IndexError('num_lst error')
    lst = await User.select_tegs_name_by_group()  # list with tag names
    build = InlineKeyboardBuilder()
    build.row(*[InlineKeyboardButton(text=teg, callback_data=teg)
                for teg in lst[num_lst]], width=1)

    if num_lst == 0:  # first list
        build.row(InlineKeyboardButton(text=lex_us.peg_but['forward'],
                                       callback_data='forward'), width=1)

    elif num_lst == len(lst) - 1:  # end list
        build.row(InlineKeyboardButton(text=lex_us.peg_but['back'],
                                       callback_data='back'), width=1)

    else:  # other list
        build.row(InlineKeyboardButton(text=lex_us.peg_but['back'],
                                       callback_data='back'),
                  InlineKeyboardButton(text=lex_us.peg_but['forward'],
                                       callback_data='forward'), width=2)

        build.row(InlineKeyboardButton(text=lex_us.peg_but['house'],
                                        callback_data='house'), width=1)
        return build.as_markup()  # type: ignore

    build.row(InlineKeyboardButton(text=lex_us.peg_but['house'],
                                    callback_data='house'), width=1)
    return build.adjust(1).as_markup()  # type: ignore


async def create_peg_kb_items(num_lst: int, teg_name: str, channels_name: str) -> InlineKeyboardMarkup:
    """Create peg table items

    Parameters
    ----------
    num_lst : int
        _description_

    Returns
    -------
    InlineKeyboardMarkup
        kb with a name items

    Raises
    ------
    IndexError
        if num_lst > 0
    """
    if num_lst < 0:
        raise IndexError('num_lst error')
    lst = await User.select_items_name_by_group(teg_name, channels_name)
    build = InlineKeyboardBuilder()
    build.row(*[InlineKeyboardButton(text=item,
                                     callback_data=item)
                for item in lst[num_lst]], width=1)

    if num_lst == 0:  # first list
        build.row(InlineKeyboardButton(text=lex_us.peg_but['forward'],
                                       callback_data='forward'), width=1)

    elif num_lst == len(lst) - 1:  # end list
        build.row(InlineKeyboardButton(text=lex_us.peg_but['back'],
                                       callback_data='back'), width=1)

    else:  # other list
        build.row(InlineKeyboardButton(text=lex_us.peg_but['back'],
                                       callback_data='back'),
                  InlineKeyboardButton(text=lex_us.peg_but['forward'],
                                       callback_data='forward'), width=2)

        build.row(InlineKeyboardButton(text=lex_us.peg_but['house'],
                                        callback_data='house'), width=1)
        return build.as_markup()  # type: ignore

    build.row(InlineKeyboardButton(text=lex_us.peg_but['house'],
                                    callback_data='house'), width=1)
    return build.adjust(1).as_markup()  # type: ignore


async def create_peg_kb_search_items(num_lst: int, name_items: str) -> InlineKeyboardMarkup:
    """Create peg table search items

    Parameters
    ----------
    num_lst : int
        list number

    Returns
    -------
    InlineKeyboardMarkup
        kb with a name item

    Raises
    ------
    IndexError
        if num_lst < 0
    """
    if num_lst < 0:
        raise IndexError('num_lst error')
    lst = await User.select_items_name(name_items)
    build = InlineKeyboardBuilder()
    build.row(*[InlineKeyboardButton(text=item,
                                     callback_data=item)
                for item in lst[num_lst]], width=1)

    if num_lst == 0:  # first list
        build.row(InlineKeyboardButton(text=lex_us.peg_but['forward'],
                                       callback_data='forward'), width=1)

    elif num_lst == len(lst) - 1:  # end list
        build.row(InlineKeyboardButton(text=lex_us.peg_but['back'],
                                       callback_data='back'), width=1)

    else:  # other list
        build.row(InlineKeyboardButton(text=lex_us.peg_but['back'],
                                       callback_data='back'),
                  InlineKeyboardButton(text=lex_us.peg_but['forward'],
                                       callback_data='forward'), width=2)

        build.row(InlineKeyboardButton(text=lex_us.peg_but['house'],
                                        callback_data='house'), width=1)
        return build.as_markup()  # type: ignore

    build.row(InlineKeyboardButton(text=lex_us.peg_but['house'],
                                    callback_data='house'), width=1)
    return build.adjust(1).as_markup()  # type: ignore


async def create_link_kb_item(link: str) -> InlineKeyboardMarkup:
    """create kb with a link to the item

    Parameters
    ----------
    link : str
        link for item

    Returns
    -------
    InlineKeyboardMarkup
        KB with a link to the item
    """    
    build = InlineKeyboardBuilder()
    build.row(InlineKeyboardButton(text=lex_us.link_text, url=link),
              InlineKeyboardButton(text=lex_us.peg_but['house'], callback_data='house'),
              width=1)
    return build.as_markup()
