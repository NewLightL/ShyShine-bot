'''State for user'''

from aiogram.fsm.state import StatesGroup, State


class SearchItem(StatesGroup):
    name_item = State()
    card_search_item = State()


class ViewCatalog(StatesGroup):
    view_tegs = State()
    view_items = State()
    card_item = State()
