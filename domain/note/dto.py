from dataclasses import dataclass
from typing import List


@dataclass
class CreateNoteDTO:
    header: str
    text: str
    tags: List[str]
    author: str
    likes: int
    comments: int
    color: int


@dataclass
class UpdateNoteDTO:
    id: int
    header: str
    text: str
    tags: List[str]
    author: str
    likes: int
    comments: int
    color: int


@dataclass
class PartiallyUpdateNoteDTO:
    id: int
    header: str = None
    text: str = None
    tags: List[str] = None
    author: str = None
    likes: int = None
    comments: int = None
    color: int = None
