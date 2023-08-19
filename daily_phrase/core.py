from pathlib import Path
from tempfile import TemporaryDirectory

from audio import AudioPhrase
from image import download_random_image_from_unsplash
from language import SPANISH, LanguageInfo
from models import Language, Phrase
from sqlmodel import Session, create_engine, select
from video import Video

DATABASE_PATH = Path(__file__).parent / "db/daily_phrase.db"
TEMPORARY_MEDIA_PATH = Path(__file__).parent / "tmp/"
STATIC_ASSET_PATH = Path(__file__).parent / "static-assets/"


def main(language: LanguageInfo) -> None:
    """Main entry point for the daily_phrase package."""
    audio_phrases = [language.introduction_audio] + _load_phrases()
    with TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)
        image_path = download_random_image_from_unsplash(language.country_name, tmp_dir)
        Video(
            image_path=image_path,
            audio_phrases=audio_phrases,
            tmp_media_dir=tmp_dir,
            language_info=language,
        )


def _load_phrases(
    *, native_language: Language, foreign_language: Language
) -> list[AudioPhrase]:
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
        for result in results:
            result.used = True
        session.commit()
    return [
        AudioPhrase(TEMPORARY_MEDIA_PATH, result.native_phrase, result.foreign_phrase)
        for result in results
    ]


if __name__ == "__main__":
    main(SPANISH)
