from pathlib import Path
from tempfile import TemporaryDirectory

from audio import AudioPhrase
from image import download_random_image_from_unsplash
from models import Country, Language, Phrase
from sqlmodel import Session, create_engine, select
from video import Video

DATABASE_PATH = Path(__file__).parent / "db/daily_phrase.db"
TEMPORARY_MEDIA_PATH = Path(__file__).parent / "tmp/"


def main(country: Country) -> None:
    """Main entry point for the daily_phrase package."""
    audio_phrases = _mock_load_phrases()
    with TemporaryDirectory() as tmp_dir:
        tmp_dir = "tmp/"
        tmp_dir = Path(tmp_dir)
        image_path = download_random_image_from_unsplash(country, tmp_dir)
        Video(image_path, audio_phrases, tmp_dir, country.background_music_path)


def _mock_load_phrases() -> list[AudioPhrase]:
    return [
        AudioPhrase(
            TEMPORARY_MEDIA_PATH,
            "I'm looking for a good book to read.",
            "Estoy buscando un buen libro para leer.",
            native_audio_path=TEMPORARY_MEDIA_PATH
            / "native_audio_-917148876481730440.mp3",
            native_audio_length=1.93,
            foreign_audio_path=TEMPORARY_MEDIA_PATH
            / "foreign_audio_-917148876481730440.mp3",
            foreign_audio_length=3.11,
        ),
        AudioPhrase(
            TEMPORARY_MEDIA_PATH,
            "I need to talk to you about something important.",
            "Necesito hablar contigo acerca de algo importante.",
            native_audio_path=TEMPORARY_MEDIA_PATH
            / "native_audio_1365006673279825515.mp3",
            native_audio_length=2.32,
            foreign_audio_path=TEMPORARY_MEDIA_PATH
            / "foreign_audio_1365006673279825515.mp3",
            foreign_audio_length=3.94,
        ),
    ]


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
    return [
        AudioPhrase(TEMPORARY_MEDIA_PATH, result.native_phrase, result.foreign_phrase)
        for result in results
    ]


if __name__ == "__main__":
    country = Country(
        name="spain",
        background_music_path=Path(__file__).parent
        / "music/sardana-by-kevin-macleod-from-filmmusic-io.mp3",
    )
    main(country)
