'''User handlers'''

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

import bot.client.keyboard as kb
import bot.client.lexicon_user as lex
from bot.client.state import SearchItem, ViewCatalog
from bot.db.user_req import User
from bot.all.keyboards import start_board
from bot.client.filter import CorrectChannels, CorrectItems, CorrectTegs


router_user = Router(name='user')


#! CATALOG
@router_user.message(CommandStart())
async def start_mess(mess: Message, state: FSMContext,
                     my_channel: dict) -> None:
    """Responds to the start command

    Parameters
    ----------
    mess : Message
    my_channel : dict
    """
    await state.clear()
    await mess.answer(lex.start_mess,
                      reply_markup=await start_board(my_channel))


@router_user.callback_query(F.data == 'house', StateFilter(ViewCatalog.view_tegs))
async def start_mess_call(call: CallbackQuery, state: FSMContext,
                          my_channel: dict) -> None:
    """Answers the "home" callback and returns the user to start

    Parameters
    ----------
    mess : Message
        _description_
    my_channel : dict
        _description_
    """
    await state.clear()
    await call.answer()
    await call.message.edit_text(lex.start_mess,  # type: ignore
                      reply_markup=await start_board(my_channel))


@router_user.callback_query(F.data == 'house', StateFilter(ViewCatalog.view_items))
async def home_items_for_tegs(call: CallbackQuery, state: FSMContext) -> None:
    """Answers the "home" callback and returns the user to selecting tags

    Parameters
    ----------
    mess : Message
    my_channel : dict
    """
    await state.update_data(num_lst=0)
    await call.answer()
    await state.set_state(ViewCatalog.view_tegs)
    await call.message.edit_text(lex.view_tegs,  # type: ignore
                      reply_markup=await kb.create_peg_kb_tegs(0))


@router_user.callback_query(F.data == 'house', StateFilter(ViewCatalog.card_item))
async def home_item_for_items(call: CallbackQuery, state: FSMContext) -> None:
    """start with call

    Parameters
    ----------
    mess : Message
    my_channel : dict
    """
    data = await state.get_data()
    await call.answer()
    await state.set_state(ViewCatalog.view_items)
    await call.message.edit_text(lex.view_tegs,  # type: ignore
                      reply_markup=await kb.create_peg_kb_items(data['num_lst'],
                                                                data['teg'],
                                                                data['channel']))


@router_user.callback_query(CorrectChannels(),
                            F.data.as_('name'))
async def view_tegs(call: CallbackQuery, state: FSMContext,
                    name: str):
    """view tegs

    Parameters
    ----------
    call : CallbackQuery
    state : FSMContext
    name : str
    """    
    await call.answer()
    await state.set_state(ViewCatalog.view_tegs)
    await state.update_data(num_lst=0, channel=name)
    await call.message.edit_text(lex.view_tegs,  # type: ignore
                                 reply_markup=await kb.create_peg_kb_tegs(0))


@router_user.callback_query(CorrectTegs(),
                            F.data.as_('name'))
async def view_items(call: CallbackQuery, state: FSMContext,
                     name: str):
    """view items

    Parameters
    ----------
    call : CallbackQuery
    state : FSMContext
    name : str
    """
    await call.answer()
    await state.set_state(ViewCatalog.view_items)
    await state.update_data(num_lst=0, teg=name)
    data = await state.get_data()
    await call.message.edit_text(lex.view_items,  # type: ignore
                        reply_markup=await kb.create_peg_kb_items(0, name, data['channel']))


@router_user.callback_query(CorrectItems(),
                            F.data.as_('name'),
                            StateFilter(ViewCatalog.view_items))
async def card_items(call: CallbackQuery, state: FSMContext,
                    name: str):
    """view one item

    Parameters
    ----------
    call : CallbackQuery
    state : FSMContext
    name : str
    """
    await call.answer()
    await state.set_state(ViewCatalog.card_item)
    await state.update_data(num_lst=0, name=name)
    data = await state.get_data()
    link = await User.select_item(name, data['channel'], data['teg'])
    await call.message.edit_text(lex.card_item.format(name),  # type: ignore
                              reply_markup=await kb.create_link_kb_item(link))  # type: ignore


@router_user.callback_query(F.data == 'back', StateFilter(ViewCatalog.view_tegs))
async def back_lst(call: CallbackQuery, state: FSMContext):
    """back list

    Parameters
    ----------
    call : CallbackQuery
    state : FSMContext
    """
    data = await state.get_data()
    await state.update_data(num_lst=data['num_lst'] - 1)
    await call.answer()

    await call.message.edit_text(lex.view_tegs,  # type: ignore
                                 reply_markup=await kb.create_peg_kb_tegs(data['num_lst'] - 1))


@router_user.callback_query(F.data == 'forward', StateFilter(ViewCatalog.view_tegs))
async def forward_lst(call: CallbackQuery, state: FSMContext):
    """forward list

    Parameters
    ----------
    call : CallbackQuery
    state : FSMContext
    """
    data = await state.get_data()
    await state.update_data(num_lst=data['num_lst'] + 1)
    await call.answer()

    await call.message.edit_text(lex.view_tegs,  # type: ignore
                                 reply_markup=await kb.create_peg_kb_tegs(data['num_lst'] + 1))


@router_user.callback_query(F.data == 'forward', StateFilter(ViewCatalog.view_items))
async def forward_lst_tegs(call: CallbackQuery, state: FSMContext):
    """forward list

    Parameters
    ----------
    call : CallbackQuery
    state : FSMContext
    """
    data = await state.get_data()
    await state.update_data(num_lst=data['num_lst'] + 1)
    await call.answer()

    await call.message.edit_text(lex.view_tegs,  # type: ignore
                                 reply_markup=await kb.create_peg_kb_items(data['num_lst'] + 1,
                                                                           data['name'],
                                                                           data['channel']))


@router_user.callback_query(F.data == 'back', StateFilter(ViewCatalog.view_items))
async def back_lst_items(call: CallbackQuery, state: FSMContext):
    """back list

    Parameters
    ----------
    call : CallbackQuery
    state : FSMContext
    """
    data = await state.get_data()
    await state.update_data(num_lst=data['num_lst'] - 1)
    await call.answer()

    await call.message.edit_text(lex.view_tegs,  # type: ignore
                                 reply_markup=await kb.create_peg_kb_items(data['num_lst'] - 1,
                                                                           data['name'],
                                                                           data['channel']))


#! SEARCH ITEMS BY NAME
@router_user.callback_query(F.data == 'search', StateFilter(default_state))
async def search_item(call: CallbackQuery,
                      state: FSMContext) -> None:
    """Search items by name

    Parameters
    ----------
    call : CallbackQuery
    state : FSMContext
    """    
    await call.answer()
    await state.clear()
    await state.set_state(SearchItem.name_item)
    await call.message.answer(lex.search['name'], reply_markup=kb.return_home) # type: ignore


@router_user.message(StateFilter(SearchItem.name_item))
async def search_item2(mess: Message,
                      state: FSMContext) -> None:
    """Search items by name

    Parameters
    ----------
    mess : Message
    state : FSMContext
    """
    await state.update_data(num_lst=0, name_items=mess.text)
    await state.set_state(SearchItem.card_search_item)
    await mess.answer(lex.view_items,
        reply_markup=await kb.create_peg_kb_search_items(0,
                                                        mess.text))  # type: ignore


@router_user.callback_query(CorrectItems(),
                            F.data.as_('name'),
                            StateFilter(SearchItem.card_search_item))
async def card_items_search(call: CallbackQuery, state: FSMContext,
                    name: str):
    """view one item

    Parameters
    ----------
    call : CallbackQuery
    state : FSMContext
    name : str
    """
    await call.answer()
    await state.set_state(SearchItem.card_search_item)
    await state.update_data(name=name)
    link = await User.select_item_link(name)
    await call.message.edit_text(lex.card_item.format(name),  # type: ignore
                              reply_markup=await kb.create_link_kb_item(link))  # type: ignore


@router_user.callback_query(F.data == 'back',
                            StateFilter(SearchItem.name_item))
async def back_lst_search_items(call: CallbackQuery, state: FSMContext):
    """back list

    Parameters
    ----------
    call : CallbackQuery
    state : FSMContext
    """
    data = await state.get_data()
    await state.update_data(num_lst=data['num_lst'] - 1)
    await call.answer()

    await call.message.edit_text(lex.view_tegs,  # type: ignore
            reply_markup=await kb.create_peg_kb_search_items(data['num_lst'] - 1,
                                                             data['name_items']))


@router_user.callback_query(F.data == 'forward',
                            StateFilter(SearchItem.name_item))
async def forward_lst_search_items(call: CallbackQuery, state: FSMContext):
    """forward list

    Parameters
    ----------
    call : CallbackQuery
    state : FSMContext
    """
    data = await state.get_data()
    await state.update_data(num_lst=data['num_lst'] + 1)
    await call.answer()

    await call.message.edit_text(lex.view_tegs,  # type: ignore
            reply_markup=await kb.create_peg_kb_search_items(data['num_lst'] + 1,
                                                             data['name_items']))


@router_user.callback_query(F.data == 'house',
                            StateFilter(SearchItem.name_item,
                                        SearchItem.card_search_item))
async def start_mess_search_call(call: CallbackQuery, state: FSMContext,
                          my_channel: dict) -> None:
    """start with call

    Parameters
    ----------
    mess : Message
    my_channel : dict
    """
    await state.clear()
    await call.answer()
    await call.message.edit_text(lex.start_mess,  # type: ignore
                      reply_markup=await start_board(my_channel))
