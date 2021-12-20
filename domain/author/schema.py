from marshmallow import Schema, post_dump
from marshmallow.fields import String


class AuthorSchema(Schema):
    name = String()

    @post_dump
    def postdump_author(self, data: dict, **kwargs):
        return data['name']
