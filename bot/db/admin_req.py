'''Admin requests'''

from typing import (
    Iterable,
    Sequence
)

from sqlalchemy import select

from bot.db.other_req import Other
from bot.db.database import async_session
from bot.db.layout import (
    Items,
    Tegs
)


class Admin:
    """Admin requsests"""
    @staticmethod
    async def select_all_tegs() -> Sequence[str]:
        """Return list with tags name

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
    async def update_tegs(tegs_id: int, new_name: str) -> None:
        """Update tegs"""
        async with async_session() as session:
            data = await session.get(Tegs, tegs_id)
            data.tegs_name = new_name  # type: ignore
            await session.flush()
            await session.commit()


    @staticmethod
    async def insert_tegs(names: Iterable[str]) -> None:
        """Inserts new tags into the table"""
        async with async_session() as session:
            data = [Tegs(tegs_name=name) for name in names]
            session.add_all(data)
            await session.flush()
            await session.commit()


    @staticmethod
    async def insert_items(name: str, tegs: str,
                           photo: str, link: str,
                           channels: str) -> None:
        """Insert new items into the table"""
        async with async_session() as session:
            # Get id_tegs and id_channels
            id_tegs = await Other.id_tegs(tegs)
            id_channels = await Other.id_channels(channels)
            # Checking the correctness of the data
            if id_channels is None:
                raise TypeError(f'{channels} not in the table')
            if id_tegs is None:
                raise TypeError(f'{tegs} not in the table')
            # Create and add new items
            data = Items(items_name=name,
                         photo=photo,
                         link=link,
                         tegs_id=id_tegs,
                         channels_id=id_channels)
            session.add(data)
            await session.flush()
            await session.commit()
