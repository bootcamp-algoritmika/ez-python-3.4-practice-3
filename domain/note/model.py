from dataclasses import field, dataclass
from datetime import datetime

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..author.model import Author
    from ..tag.model import Tag
    

from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func, Table, Text

from ..mapper import metadata, mapper_registry


@dataclass
class Note:
    id: int = field(init=False)
    header: str = None
    text: str = None
    tags: list = field(default_factory=list)
    author: Any = None
    likes: int = None
    comments: int = None
    color: int = None
    created_date: datetime = None
    modified_date: datetime = None


note_table = Table(
    'note', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('header', String),
    Column('likes', Integer),
    Column('text', Text),
    Column("author_id", Integer, ForeignKey("author.id")),
    Column('created_date', TIMESTAMP, server_default=func.now()),
    Column('modified_date', TIMESTAMP, server_default=func.now(), onupdate=func.now())
)
mapper_registry.map_imperatively(
    Note, note_table
)
