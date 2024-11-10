'''Other handlers'''

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import bot.other.lexicon_other as lex
from bot.all.keyboards import channel_board


router_other = Router(name='other')


@router_other.message(Command('help'))
async def answer_help(mess: Message, my_channel: dict) -> None:
    """Responds to the help command

    Parameters
    ----------
    mess : Message
    my_channel : dict
    """
    await mess.answer(lex.help_mess, reply_markup=await channel_board(my_channel=my_channel))


@router_other.message()
async def answer_other_text(mess: Message) -> None:
    """Replies to other messages

    Parameters
    ----------
    mess : Message
    """
    await mess.answer('Я отвечаю только на команды')
