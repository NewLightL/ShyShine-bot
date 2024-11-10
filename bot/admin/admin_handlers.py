'''Admin handlers for bot'''

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.enums.message_entity_type import MessageEntityType

import bot.admin.keyboard as kb
from bot.all.keyboards import every_post
import bot.admin.lexicon_admin as lex
import bot.all.lexicon_all as lexicon
from bot.admin.state import SendPost, SendPostPere
from bot.all.keyboards import channel_board
from bot.admin.filter import ChannelCorrect
from bot.db.admin_req import Admin


router_admin = Router(name='admin')  # create router for admin


@router_admin.message(Command('cancel'), ~StateFilter(default_state))
@router_admin.message(StateFilter(SendPost.repeat, SendPostPere.y_n),
                      F.text == lexicon.LEXICON['no'])
async def cancel_state_true(mess: Message, state: FSMContext) -> None:
    """Clears the state if the user is in it

    Parameters
    ----------
    mess : Message
        This object represents a message
    state : FSMContext
        State machine
    """
    await mess.answer(lex.cancel['true'],
                      reply_markup=kb.remove)
    await state.clear()


@router_admin.message(Command('cancel'), StateFilter(default_state))
async def cancel_state_false(mess: Message) -> None:
    """The user submitted /cancel but he is unable to create a post

    Parameters
    ----------
    mess : Message
        This object represents a message
    """
    await mess.answer(lex.cancel['false'],
                      reply_markup=kb.remove)


@router_admin.message(Command('admin_help'))
async def send_help(mess: Message) -> None:
    """answer help

    Parameters
    ----------
    mess : Message
    """
    await mess.answer(lex.help_mess)


@router_admin.message(Command('send_post_pere'))
async def send_post_pere(mess: Message, state: FSMContext, my_channel) -> None:
    """send post

    Parameters
    ----------
    mess : Message
    state : FSMContext
    my_channel : dict
    """
    await state.clear()
    await mess.answer(lex.state['repeat'].format('ShyShine_pere'),
                      reply_markup=kb.yes_no)
    await mess.answer(lex.pere, reply_markup=await channel_board(my_channel))
    await state.set_state(SendPostPere.y_n)


@router_admin.message(StateFilter(SendPostPere.y_n))
async def send_post_pere2(mess: Message, state: FSMContext, my_channel) -> None:
    await mess.bot.send_message(chat_id=my_channel['@']['pere'],  # type: ignore
                                text=lex.pere,
                                reply_markup=await channel_board(my_channel))
    await state.clear()
    await mess.answer(lex.state['post_send'], reply_markup=kb.remove)


@router_admin.message(Command('send_post'))
async def send_post(mess: Message, state: FSMContext,
                    my_channel: dict[str, dict[str, str]]) -> None:
    """Start sending the post.\n
    Selecting the channel where the post will be sent

    Parameters
    ----------
    mess : Message
        This object represents a message
    state : FSMContext
        State machine
    my_channel : dict[str: dict[str, str]]
        dictionary with channel names
    """
    await state.clear()
    await mess.answer(lex.state['help'],
                      reply_markup=kb.remove)

    await mess.answer(lex.state['channel'],
                      reply_markup=await kb.create_kb(my_channel))

    await state.set_state(SendPost.channel)


@router_admin.message(StateFilter(SendPost.channel),
                      ChannelCorrect())
async def send_post2(mess: Message, state: FSMContext,
                     my_channel) -> None:
    """save channel in data"""
    await state.update_data(channel=my_channel['@'][mess.text])
    await mess.answer(lex.state['media'], reply_markup=kb.remove)
    await state.set_state(SendPost.media)


@router_admin.message(StateFilter(SendPost.channel))
async def send_post2_incor(mess: Message) -> None:
    """save channel in data"""
    await mess.answer(lex.state['incorrect'])


@router_admin.message(StateFilter(SendPost.media), F.video)
@router_admin.message(StateFilter(SendPost.media), F.photo)
@router_admin.message(StateFilter(SendPost.media), F.text)
async def send_post3(mess: Message, state: FSMContext) -> None:
    """save channel in data"""
    flag = False
    if mess.text:
        enti = mess.entities or []
        for item in enti:
            if item.type == MessageEntityType.URL:
                url = item.extract_from(mess.text)
                await state.update_data(media=url)
                if url.split('.')[-1] in ('mp4', ):
                    await state.update_data(type_media='video')
                else:
                    await state.update_data(type_media='photo')
                flag = True
    if mess.photo:
        await state.update_data(media=mess.photo[-1].file_id)
        await state.update_data(type_media='photo')
        flag = True
    if mess.video:
        await state.update_data(media=mess.video.file_id)
        await state.update_data(type_media='video')
        flag = True
    if flag:
        await mess.answer(lex.state['name'])
        await state.set_state(SendPost.name)
        return
    await mess.answer(lex.state['incorrect'])


@router_admin.message(StateFilter(SendPost.name))
async def send_post4(mess: Message, state: FSMContext) -> None:
    """save channel in data"""
    await state.update_data(name=mess.text.strip())  # type: ignore
    await mess.answer(lex.state['desc'])
    await state.set_state(SendPost.desc)


@router_admin.message(StateFilter(SendPost.desc))
async def send_post5(mess: Message, state: FSMContext) -> None:
    """save channel in data"""
    await state.update_data(desc=mess.text.strip())  # type: ignore
    await mess.answer(lex.state['site'])
    await state.set_state(SendPost.site)


@router_admin.message(StateFilter(SendPost.site))
async def send_post6(mess: Message, state: FSMContext) -> None:
    """save channel in data"""
    await state.update_data(site=mess.text)
    await mess.answer(lex.state['teg'],
                      reply_markup=await kb.create_kb_tegs())
    await state.set_state(SendPost.teg)


@router_admin.message(StateFilter(SendPost.teg))
async def send_post7(mess: Message, state: FSMContext,
                     my_channel) -> None:
    """save channel in data"""
    if mess.text.count('#') != 1:  # type: ignore
        await mess.answer(lex.state['incorrect'])
        return
    await state.update_data(teg=mess.text)
    data: dict[str, str] = await state.get_data()
    form = (data['name'], data['desc'],
            (f'<a href="{data['site']}">тык*</a>' if
             not data['site'].isdigit()
             else f'<code>{data['site']}</code>'),
            data['teg'])
    await mess.answer(lex.state['repeat'].format(data['channel']), reply_markup=kb.yes_no)
    if data['type_media'] == 'video':
        await mess.answer_video(video=data['media'],  # type: ignore
                                caption=lexicon.POST.format(*form),
                                reply_markup=await every_post(my_channel))
    else:
        await mess.answer_photo(photo=data['media'],
                                caption=lexicon.POST.format(*form),
                                reply_markup=await every_post(my_channel))
    await state.set_state(SendPost.repeat)


@router_admin.message(StateFilter(SendPost.repeat))
async def send_post8(mess: Message, state: FSMContext,
                     my_channel: dict) -> None:
    """save channel in data"""
    data: dict[str, str] = await state.get_data()
    form = (data['name'], data['desc'],
            (f'<a href="{data['site']}">тык*</a>' if
             not data['site'].isdigit()
             else f'<code>{data['site']}</code>'),
            data['teg'])
    if data['type_media'] == 'video':
        new = await mess.bot.send_video(chat_id=data['channel'],  # type: ignore
                                  video=data['media'],  # type: ignore
                                  caption=lexicon.POST.format(*form),
                                  reply_markup=await every_post(my_channel))
    else:
        new = await mess.bot.send_photo(chat_id=data['channel'],  # type: ignore
                                  photo=data['media'],  # type: ignore
                                  caption=lexicon.POST.format(*form),
                                  reply_markup=await every_post(my_channel))
    # Work with db
    def get_values(value, dct: dict[str, str]) -> str | None:
        for key, val in dct.items():
            if val == value:
                return key
        return None

    link: str = f't.me/{new.chat.username}/{new.message_id}'
    channel = get_values(data['channel'], my_channel['@'])
    await Admin.insert_items(data['name'], data['teg'],
                             data['media'], link, channel)  # type: ignore

    await mess.answer(lex.state['post_send'],
                      reply_markup=kb.remove)
    await state.clear()
