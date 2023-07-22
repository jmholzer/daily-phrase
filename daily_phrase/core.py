
from pathlib import Path


from audio import AudioPhrase


from image import download_random_image_from_unsplash
from tempfile import TemporaryDirectory

from sqlmodel import Session, select, create_engine
from models import Phrase


DATABASE_PATH = Path(__file__).parent / "db/daily_phrase.db"


def main(language: str, country: str) -> None:
    """Main entry point for the daily_phrase package.
    """
    audio_phrases = _load_phrases()  # TODO: implement this function
    with TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)
        download_random_image_from_unsplash(country, tmp_dir)


def _load_phrases(*, native_language: str, foreign_language: str) -> list[AudioPhrase]:
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
            .limit(3)
        )
        results = session.exec(query).all()
    return [
        AudioPhrase(
            Path(__file__).parent / "tmp/",
            result.native_phrase,
            result.foreign_phrase
        )
        for result in results
    ]


if __name__ == "__main__":
    _load_phrases(native_language="english", foreign_language="spanish")
