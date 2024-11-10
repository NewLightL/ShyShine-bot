""""Settings for database"""

from typing import Annotated

from sqlalchemy import (
    String
)
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column
)

from bot.db.sett import settings


async_engine = create_async_engine(url=settings.db_url)
async_session = async_sessionmaker(async_engine)

IntPK = Annotated[int, mapped_column(primary_key=True)]
Str80 = Annotated[str, String(80)]


class Base(DeclarativeBase):
    """Base for db"""
    type_annotation_map = {
        IntPK: mapped_column(primary_key=True),
        Str80: String(80)
    }
