from dataclasses import dataclass
from pathlib import Path

from audio import CachedAudioPhrase

STATIC_ASSET_PATH = Path(__file__).parent / "static-assets/"


@dataclass
class LanguagePair:
    """
    Representation of a language necessary to create a video.
    """

    native_language: str
    foreign_language: str
    country_name: str
    background_music_path: Path
    introduction_audio: CachedAudioPhrase


SPANISH = LanguagePair(
    native_language="english",
    foreign_language="spanish",
    country_name="Spain",
    background_music_path=Path(
        "static-assets/music/sardana-by-kevin-macleod-from-filmmusic-io.mp3"
    ),
    introduction_audio=CachedAudioPhrase(
        native_phrase="Hello, here are two Spanish phrases for you to learn today.",
        foreign_phrase="Hola, aquí tienes dos frases en español para aprender hoy.",
        native_audio_path=STATIC_ASSET_PATH
        / "introductions/spanish_introduction_english.mp3",
        foreign_audio_path=STATIC_ASSET_PATH
        / "introductions/spanish_introduction_spanish.mp3",
        native_audio_length=3.71,
        foreign_audio_length=6.64,
    ),
)
