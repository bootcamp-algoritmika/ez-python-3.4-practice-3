from datetime import datetime

from marshmallow import Schema
from marshmallow.fields import String, Integer, DateTime, Nested

from ..tag.schema import TagSchema
from ..author.schema import AuthorSchema


class NoteSchema(Schema):
    id: int = Integer()
    header: str = String()
    text: str = String()
    likes: int = Integer()
    tags: list[str] = Nested(TagSchema, many=True)
    author: str = Nested(AuthorSchema)
    comments: int = Integer()
    color: int = Integer()
    created_date: datetime = DateTime()
    modified_date: datetime = DateTime()
