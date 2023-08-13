
from pathlib import Path


from audio import AudioPhrase


from image import download_random_image_from_unsplash
from tempfile import TemporaryDirectory

from sqlmodel import Session, select, create_engine
from models import Phrase, Language, Country


DATABASE_PATH = Path(__file__).parent / "db/daily_phrase.db"
TEMPORARY_MEDIA_PATH = Path(__file__).parent / "tmp/"


def main(native_language: Language, foreign_language: Language, country: Country) -> None:
    """Main entry point for the daily_phrase package.
    """
    audio_phrases = _load_phrases()
    with TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)
        download_random_image_from_unsplash(country, tmp_dir)


def _load_phrases(*, native_language: Language, foreign_language: Language) -> list[AudioPhrase]:
    engine = create_engine(f"sqlite:///{DATABASE_PATH}")
    with Session(engine) as session:
        query = (
            select(Phrase)
            .where(
                Phrase.used == False
                and Phrase.native_language == native_language
                and Phrase.foreign_language == foreign_language
            )
            .order_by(Phrase.id)
            .limit(1)
        )
        results = session.exec(query).all()
    return [
        AudioPhrase(
            TEMPORARY_MEDIA_PATH,
            result.native_phrase,
            result.foreign_phrase
        )
        for result in results
    ]


if __name__ == "__main__":
    main(Language.ENGLISH, Language.SPANISH, Country.Spain)
