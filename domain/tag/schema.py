from marshmallow import Schema, post_dump
from marshmallow.fields import String


class TagSchema(Schema):
    name = String()

    @post_dump
    def postdump_tag(self, data: dict, **kwargs):
        return data['name']
