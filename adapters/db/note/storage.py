from typing import Any

from sqlalchemy import or_
from sqlalchemy.orm import subqueryload

from domain.author.model import Author
from domain.note.exceptions import NoteNotFoundException
from domain.note.model import Note
from domain.note.storage import NoteStorageI
from domain.note.dto import UpdateNoteDTO, PartiallyUpdateNoteDTO, CreateNoteDTO
from domain.tag.model import Tag
from adapters.db.db_init import Session


class NoteStorage(NoteStorageI):

    def create(self, note: CreateNoteDTO) -> int:
        with Session() as session:
            new_note = Note(
                header=note.header,
                text=note.text,
                likes=note.likes,
                color=note.color,
                comments=note.comments,
                author=self.get_author(session=session, author=note.author),
                tags=self.get_tags(session=session, tags=note.tags)
            )
            session.add(new_note)
            session.flush()
            new_note_id = new_note.id
            session.commit()
        return new_note_id

    def update(self, note: UpdateNoteDTO) -> None:
        with Session() as session:
            note_query: Note = session.query(Note).filter(Note.id == note.id).one_or_none()
            if not note_query:
                raise NoteNotFoundException(message="note not found")
            note_query.header = note.header
            note_query.text = note.text
            note_query.likes = note.likes
            note_query.comments = note.comments
            note_query.color = note.color
            note_query.tags = self.get_tags(tags=note.tags, session=session)
            note_query.author = self.get_author(author=note.author, session=session)
            session.flush()
            session.commit()

    def partial_update(self, note: PartiallyUpdateNoteDTO) -> None:
        with Session() as session:
            note_query: Note = session.query(Note).filter(Note.id == note.id).one_or_none()
            if not note_query:
                raise NoteNotFoundException(message="note not found")
            if note.header is not None:
                note_query.header = note.header
            if note.text is not None:
                note_query.text = note.text
            if note.likes is not None:
                note_query.likes = note.likes
            if note.comments is not None:
                note_query.comments = note.comments
            if note.color is not None:
                note_query.color = note.color
            if note.tags is not None:
                note_query.tags = self.get_tags(tags=note.tags, session=session)
            if note.author is not None:
                note_query.author = self.get_author(author=note.author, session=session)
            session.flush()
            session.commit()

    def delete(self, note_id: int) -> None:
        with Session() as session:
            issue_query = session.query(Note).filter(Note.id == note_id).one_or_none()
            if not issue_query:
                raise NoteNotFoundException(message="note not found")
            session.delete(issue_query)
            session.commit()

    def get_one(self, note_id: str) -> Note:
        with Session() as session:
            issue_query = session.query(Note).options(
                subqueryload(Note.tags),
                subqueryload(Note.author),
            ).filter(Note.id == note_id).one_or_none()
            if not issue_query:
                raise NoteNotFoundException(message="note not found")
        return issue_query

    def get_all(self, limit: int, offset: int, filters: dict) -> list[Note]:
        with Session() as session:
            if not filters:
                notes = session.query(Note).options(
                    subqueryload(Note.tags),
                    subqueryload(Note.author),
                ).offset(offset).limit(limit).all()
                return notes

            query = session.query(Note)
            for filter_name, filter_list in filters.items():
                if filter_name == 'header_filter':
                    operation, value = filter_list
                    if operation == 'eq':
                        query = query.filter(Note.header == value)
                    elif operation == 'like':
                        query = query.filter(Note.header.like(f'%{value}%'))
                elif filter_name == 'tags_filter':
                    values = filter_list[0]
                    values = values.split(',')
                    one_of_tag = Note.tags.any(name=values[0])
                    for value in values[1:]:
                        one_of_tag = or_(one_of_tag, Note.tags.any(name=value))
                    query = query.filter(one_of_tag)
                elif filter_name == 'likes_filter':
                    operation, value = filter_list
                    query = self.apply_number_filter(
                        column=Note.likes,
                        query=query,
                        operation=operation,
                        value=value
                    )
                elif filter_name == 'comments_filter':
                    operation, value = filter_list
                    query = self.apply_number_filter(
                        column=Note.comments,
                        query=query,
                        operation=operation,
                        value=value
                    )
            notes = query.options(
                subqueryload(Note.tags),
                subqueryload(Note.author),
            ).offset(offset).limit(limit).all()

        return notes

    def get_tags(self, session: Session, tags: list[str]) -> list[Tag]:
        query_tags: list[Tag] = []
        for tag in tags:
            query_tag = session.query(Tag).filter(Tag.name == tag).one_or_none()
            if not query_tag:
                session.add(Tag(name=tag))
                session.flush()
                query_tag = session.query(Tag).filter(Tag.name == tag).first()
            query_tags.append(query_tag)
        return query_tags

    def get_author(self, session: Session, author: str) -> Author:
        author_query = session.query(Author).filter(Author.name == author).one_or_none()
        if not author_query:
            session.add(Author(name=author))
            session.flush()
            author_query = session.query(Author).filter(Author.name == author).first()
        return author_query

    def apply_number_filter(self, column: Any, query: Any,  operation: str, value: str):
        value = int(value)
        if operation == "gt":
            query = query.filter(column > value)
        elif operation == "gte":
            query = query.filter(column >= value)
        elif operation == "lt":
            query = query.filter(column < value)
        elif operation == "lte":
            query = query.filter(column <= value)
        elif operation == "eq":
            query = query.filter(column == value)
        return query
