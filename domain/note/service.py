from typing import List

from adapters.interfaces import NoteServiceI
from domain.note.dto import CreateNoteDTO, UpdateNoteDTO, PartiallyUpdateNoteDTO
from domain.note.model import Note
from domain.note.storage import NoteStorageI


class NoteService(NoteServiceI):
    def __init__(self, storage: NoteStorageI):
        self.storage = storage

    def get_notes(self, filters: dict, limit: int, offset: int) -> List[Note]:
        dict_filters = self.get_filter_data(filters=filters)
        notes = self.storage.get_all(
            limit=limit,
            offset=offset,
            filters=dict_filters
        )
        return notes

    def get_note(self, note_id) -> Note:
        return self.storage.get_one(note_id=note_id)

    def create_note(self, note: CreateNoteDTO) -> int:
        return self.storage.create(note=note)

    def delete_note(self, note_id) -> None:
        return self.storage.delete(note_id=note_id)

    def update_note(self, note: UpdateNoteDTO):
        return self.storage.update(note=note)

    def partially_update(self, note: PartiallyUpdateNoteDTO):
        return self.storage.partial_update(note=note)

    def get_filter_data(self, filters: dict) -> dict:
        header_filter = filters.get("header")
        tags_filter = filters.get("tag")
        likes_filter = filters.get("likes")
        comments_filter = filters.get("comments")
        result_filter = {}
        if header_filter is not None:
            op, val = header_filter.split(":")
            result_filter['header_filter'] = [op, val]
        if tags_filter is not None:
            # only IN operator available
            _, val = tags_filter.split(":")
            result_filter['tags_filter'] = [val]
        if likes_filter is not None:
            op, val = likes_filter.split(":")
            result_filter['likes_filter'] = [op, val]
        if comments_filter is not None:
            op, val = comments_filter.split(":")
            result_filter['comments_filter'] = [op, val]
        return result_filter
