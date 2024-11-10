"""Other requests"""

from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import mapped_column

from bot.db.layout import (
    Channels,
    Tegs,
    Base
)
from bot.db.database import (
    async_engine,
    async_session
)


IntPK = Annotated[int, mapped_column(primary_key=True)]

class Other:
    """Other requests"""
    @staticmethod
    async def create_table() -> None:
        """Creates all tables and places information in them"""
        async with async_engine.begin() as conn:
            # Creates all tables
            await conn.run_sync(Base.metadata.create_all)

        async with async_session() as session:
            # Inserts the channel name
            session.add_all([Channels(channels_name='wildberries'),
                             Channels(channels_name='ozon'),
                             Channels(channels_name='aliexpress')])
            await session.flush()
            # Get tegs name from other file
            with open(r'bot\db\teg.txt', 'rt', encoding='utf-8') as file:
                names = [el.strip()[1:] for el in file.readlines()]
            # Inserts the tegs name
            data = [Tegs(tegs_name=name) for name in names]
            session.add_all(data)
            await session.flush()
            await session.commit()


    @staticmethod
    async def drop_table() -> None:
        """Drop table"""
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


    @staticmethod
    async def id_channels(channels: str) -> IntPK | None:
        """Return id channels from table

        Parameters
        ----------
        channels : str
            name channels

        Returns
        -------
        intpk | None
            id channels
        """
        async with async_session() as session:
            query = select(Channels.channels_id).filter(Channels.channels_name == channels.strip())
            result = await session.execute(query)
            return result.scalar()


    @staticmethod
    async def id_tegs(tegs: str) -> IntPK | None:
        """Return id tegs from table

        Parameters
        ----------
        tegs : str
            tegs name

        Returns
        -------
        IntPK | None
            tegs id
        """
        async with async_session() as session:
            if tegs.startswith('#'):
                query = select(Tegs.tegs_id).filter(Tegs.tegs_name == tegs[1:].strip())
                result = await session.execute(query)
                return result.scalar()
            query = select(Tegs.tegs_id).filter(Tegs.tegs_name == tegs.strip())
            result = await session.execute(query)
            return result.scalar()
