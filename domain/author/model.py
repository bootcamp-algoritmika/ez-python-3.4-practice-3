from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import relationship

from ..mapper import mapper_registry, metadata
from ..note.model import Note


@dataclass
class Author:
    id: int = field(init=False)
    name: str = None
    notes: list[Note] = field(default_factory=list)


author_table = Table(
    'author', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
)
mapper_registry.map_imperatively(
    Author, author_table,
    properties={
        'notes': relationship(Note, lazy='subquery', backref='author')
    }
)
