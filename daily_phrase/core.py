from pathlib import Path
from tempfile import TemporaryDirectory

from audio import AudioPhrase
from image import download_random_image_from_unsplash
from language import SPANISH, LanguagePair
from models import Phrase
from sqlmodel import Session, create_engine, select
from video import Video
from upload import upload_to_s3

DATABASE_PATH = Path(__file__).parent / "db/daily_phrase.db"
TEMPORARY_MEDIA_PATH = Path(__file__).parent / "tmp/"
STATIC_ASSET_PATH = Path(__file__).parent / "static-assets/"
NUMBER_OF_PHRASES = 2


def main(language_pair: LanguagePair) -> None:
    """Main entry point for the daily_phrase package."""
    audio_phrases = [language_pair.introduction_audio] + _load_phrases(language_pair)
    with TemporaryDirectory() as tmp_dir:
        image_path = download_random_image_from_unsplash(
            language_pair.country_name, Path(tmp_dir)
        )
        video = Video(
            image_path=image_path,
            audio_phrases=audio_phrases,
            tmp_media_dir=Path(tmp_dir),
            language_info=language_pair,
        )
        upload_to_s3(video.video_path, language_pair)


def _load_phrases(language_pair: LanguagePair) -> list[AudioPhrase]:
    with _create_session() as session:
        results = _fetch_query_results(session, language_pair)
        _validate_results(results, language_pair)
        phrases = _convert_to_phrases(results)
        session.commit()

    return [
        AudioPhrase(TEMPORARY_MEDIA_PATH, native_phrase, foreign_phrase)
        for native_phrase, foreign_phrase in phrases
    ]


def _create_session() -> Session:
    engine = create_engine(f"sqlite:///{DATABASE_PATH}")
    return Session(engine)


def _fetch_query_results(session: Session, language_pair: LanguagePair):
    query = (
        select(Phrase)
        .where(
            Phrase.used == False  # noqa: E712
            and Phrase.native_language == language_pair.native_language
            and Phrase.foreign_language == language_pair.foreign_language
        )
        .order_by(Phrase.id)
        .limit(NUMBER_OF_PHRASES)
    )
    return session.exec(query).all()


def _validate_results(results, language_pair: LanguagePair):
    if len(results) < NUMBER_OF_PHRASES:
        raise ValueError(
            f"Only {len(results)} phrases found for language pair "
            f"({language_pair.native_language}, {language_pair.foreign_language})"
        )


def _convert_to_phrases(results):
    phrases = []
    for result in results:
        phrases.append((result.native_phrase, result.foreign_phrase))
        result.used = True
    return phrases


if __name__ == "__main__":
    main(SPANISH)
