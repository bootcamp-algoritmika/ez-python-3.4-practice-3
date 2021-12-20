from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from ..mapper import mapper_registry, metadata
from ..note.model import Note

note_tags_table = Table(
    'note_tags_table', metadata,
    Column('notes_id', Integer, ForeignKey('note.id'), primary_key=True),
    Column('tags_id', Integer, ForeignKey('tag.id'), primary_key=True)
)


@dataclass
class Tag:
    id: int = field(init=False)
    name: str = None
    notes: list[Note] = field(default_factory=list)


tag_table = Table(
    'tag', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
)

mapper_registry.map_imperatively(
    Tag, tag_table,
    properties={
        'notes': relationship(Note, secondary=note_tags_table, lazy='subquery', backref='tags')
    }
)

