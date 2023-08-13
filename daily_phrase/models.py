from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class Language(str, Enum):
    """
    The set of supported languages for translations.
    """

    ENGLISH = "english"
    SPANISH = "spanish"


class Country(str, Enum):
    """
    The set of supported countries for video media.
    """

    SPAIN = "spain"


class Phrase(SQLModel, table=True):
    """
    Phrase represents the SQL table that stores phrases with their translations.,
    where a single row is a mapping of a native language phrase to a foreign language phrase.
    """

    # By default SQLModel will use the class name as the table name.
    # We can override this by setting the __tablename__ attribute to the pluralized form of the class name.
    __tablename__: str = "phrases"

    id: Optional[int] = Field(default=None, primary_key=True)
    foreign_language: Language
    foreign_phrase: str
    native_language: Language
    native_phrase: str
    used: bool = False
