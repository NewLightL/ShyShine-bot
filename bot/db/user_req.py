'''User requests'''

from typing import Sequence

from sqlalchemy import select, func

from bot.db.database import async_session
from bot.db.layout import (
    Items,
    Channels,
    Tegs
)
from bot.db.other_req import Other


class User:
    """User requests"""
    @staticmethod
    async def select_items_name(name_items: str) -> list[list[str]]:
        """Return items

        Parameters
        ----------
        name_items : str
            name items

        Returns
        -------
        Sequence[Items]
            items
        """        
        async with async_session() as session:
            query = (select(Items.items_name).
                     where(func.starts_with(Items.items_name,
                                            name_items)))
            res = await session.execute(query)
            new = res.scalars().all()
            lst = []
            inner = []
            for el in new:
                if len(inner) > 4:
                    lst.append(inner)
                    inner = []
                inner.append(el)
            lst.append(inner)
            return lst


    @staticmethod
    async def select_item_link(item_name: str) -> str|None:
        """Return link

        Parameters
        ----------
        name_items : str
            name items

        Returns
        -------
        Sequence[Items]
            items
        """        
        async with async_session() as session:
            query = select(Items.link).filter(Items.items_name == item_name)
            res = await session.execute(query)
            return res.scalar()


    @staticmethod
    async def select_items_all() -> Sequence[str]:
        """Return items

        Parameters
        ----------
        name_items : str
            name items

        Returns
        -------
        Sequence[Items]
            items
        """        
        async with async_session() as session:
            query = select(Items.items_name)
            res = await session.execute(query)
            return res.scalars().all()


    @staticmethod
    async def select_tegs_name_by_group() -> list[list[str]]:
        """for peg

        Returns
        -------
        list[str]
            list with list with tags name
        """        
        async with async_session() as session:
            query = select(Tegs.tegs_name)
            res = await session.execute(query)
            new = res.scalars().all()
            lst = []
            inner = []
            for el in new:
                if len(inner) > 4:
                    lst.append(inner)
                    inner = []
                inner.append(el)
            lst.append(inner)
            return lst


    @staticmethod
    async def select_items_name_by_group(tegs_name: str, channels_name: str) -> list[list[str]]:
        """for peg

        Returns
        -------
        list[str]
            list with list with items name
        """
        async with async_session() as session:
            query = (select(Items.items_name).
                     filter(Items.tegs_id == await Other.id_tegs(tegs_name),
                            Items.channels_id == await Other.id_channels(channels_name)))
            res = await session.execute(query)
            new = res.scalars().all()
            lst = []
            inner = []
            for el in new:
                if len(inner) > 5:
                    lst.append(inner)
                    inner = []
                inner.append(el)
            lst.append(inner)
            return lst


    @staticmethod
    async def select_item(name: str, channel: str, teg: str) -> str|None:
        """select link item

        Parameters
        ----------
        name : str
            item name
        channel : str
            channel where to look for the item
        teg : str
            tag where to look for the item

        Returns
        -------
        str|None
            link item
        """        
        async with async_session() as session:
            query = select(Items.link).where(Items.channels_id == await Other.id_channels(channel),
                                              Items.tegs_id == await Other.id_tegs(teg),
                                              Items.items_name == name)
            res = await session.execute(query)
            return res.scalar()


    @staticmethod
    async def select_tegs_name() -> Sequence[str]:
        """select all tags name

        Returns
        -------
        Sequence[str]
            list with tags name
        """        
        async with async_session() as session:
            query = select(Tegs.tegs_name)
            res = await session.execute(query)
            return res.scalars().all()


    @staticmethod
    async def select_channels_name() -> Sequence[str]:
        """select all channel name

        Returns
        -------
        Sequence[str]
            list with channels name
        """
        async with async_session() as session:
            query = select(Channels.channels_name)
            res = await session.execute(query)
            return res.scalars().all()
