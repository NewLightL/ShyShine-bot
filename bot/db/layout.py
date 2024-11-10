'''Layout database'''

from typing import Annotated

from sqlalchemy.orm import (
    mapped_column,
    Mapped
)
from sqlalchemy import ForeignKey

from bot.db.database import Base


IntPK = Annotated[int, mapped_column(primary_key=True)]


class Channels(Base):
    __tablename__ = 'channels'

    channels_id: Mapped[IntPK]
    channels_name: Mapped[str]

    def __repr__(self) -> str:
        return f'Channels(channels_id={self.channels_id!r},'\
            f' channels_name={self.channels_name!r})'


class Tegs(Base):
    __tablename__ = 'tegs'

    tegs_id: Mapped[IntPK]
    tegs_name: Mapped[str]

    def __repr__(self) -> str:
        return f'Tegs(tegs_id={self.tegs_id!r},'\
            f' tegs_name={self.tegs_name!r})'


class Items(Base):
    __tablename__ = 'items'

    items_id: Mapped[IntPK]
    items_name: Mapped[str]
    photo: Mapped[str]
    link: Mapped[str]
    channels_id: Mapped[int] = mapped_column(ForeignKey(Channels.channels_id))
    tegs_id: Mapped[int] = mapped_column(ForeignKey(Tegs.tegs_id))

    def __repr__(self) -> str:
        return f'Items(items_id={self.items_id!r},'\
                f' items_name={self.items_name!r},'\
                f' photo={self.photo!r},'\
                f' link={self.link!r},'\
                f' channels_id={self.channels_id!r},'\
                f' tegs_id={self.tegs_id!r})'
