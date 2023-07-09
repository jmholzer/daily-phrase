from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class Language(str, Enum):
    """
    The set of supported languages for translations.
    """

    ENGLISH = "english"
    SPANISH = "spanish"
    GERMAN = "german"
    ITALIAN = "italian"
    FRENCH = "french"
    PORTUGUESE = "portuguese"
    HINDI = "hindi"


class Phrases(SQLModel, table=True):
    """
    The Phrases model represents the SQL table that stores phrases with their translations.,
    where a single row is a mapping of a native language phrase to a foreign language phrase.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    foreign_language: Language
    native_language: Language
    foreign_phrase: str
    native_phrase: str
    used: bool = False
