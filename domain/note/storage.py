from abc import ABC, abstractmethod

from domain.note.model import Note
from domain.note.dto import UpdateNoteDTO, PartiallyUpdateNoteDTO, CreateNoteDTO


class NoteStorageI(ABC):

    @abstractmethod
    def get_one(self, note_id: int) -> Note:
        pass

    @abstractmethod
    def get_all(self, limit: int, offset: int, filters: dict) -> list[Note]:
        pass

    @abstractmethod
    def create(self, note: CreateNoteDTO) -> Note:
        pass

    @abstractmethod
    def update(self, note: UpdateNoteDTO) -> None:
        pass

    @abstractmethod
    def partial_update(self, note: PartiallyUpdateNoteDTO) -> None:
        pass

    @abstractmethod
    def delete(self, note_id: int) -> None:
        pass
