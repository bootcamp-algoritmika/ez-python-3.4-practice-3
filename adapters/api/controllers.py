import json

import falcon

from adapters.interfaces import NoteServiceI
from domain.note.dto import UpdateNoteDTO, PartiallyUpdateNoteDTO, CreateNoteDTO
from domain.note.exceptions import NoteNotFoundException
from domain.note.schema import NoteSchema


class NoteResource:
    def __init__(self, service: NoteServiceI):
        self.service = service

    def on_get(self, req, resp, note_id):
        try:
            note = self.service.get_note(note_id=note_id)
        except NoteNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        schema = NoteSchema()
        resp.body = json.dumps(schema.dump(note))
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, note_id):
        updated_note = req.media
        dto = UpdateNoteDTO(id=note_id, **updated_note)
        try:
            self.service.update_note(dto)
        except NoteNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204

    def on_patch(self, req, resp, note_id):
        patched_note = req.media
        dto = PartiallyUpdateNoteDTO(id=note_id, **patched_note)
        try:
            self.service.partially_update(dto)
        except NoteNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204

    def on_delete(self, req, resp, note_id):
        try:
            self.service.delete_note(note_id)
        except NoteNotFoundException as e:
            raise falcon.HTTPNotFound(title=e.message)
        resp.status = falcon.HTTP_204


class NotesResource:
    def __init__(self, service: NoteServiceI):
        self.service = service

    def on_get(self, req, resp):
        limit = req.get_param_as_int('limit') or 50
        offset = req.get_param_as_int('offset') or 0

        header_filter = req.get_param('header') or None
        tags_filter = req.get_param('tag') or None
        likes_filter = req.get_param('likes') or None
        comments_filter = req.get_param('comments') or None
        filters = {}
        if header_filter is not None:
            filters["header"] = header_filter
        if tags_filter is not None:
            filters["tag"] = tags_filter
        if likes_filter is not None:
            filters["likes"] = likes_filter
        if comments_filter is not None:
            filters["comments"] = comments_filter

        notes = self.service.get_notes(filters=filters, limit=limit, offset=offset)

        schema = NoteSchema()
        dict_notes = schema.dump(notes, many=True)
        resp.body = json.dumps(dict_notes)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        data = req.get_media()
        new_note = CreateNoteDTO(**data)
        note_id = self.service.create_note(new_note)
        resp.status = falcon.HTTP_201
        resp.location = f'/notes/{note_id}'
