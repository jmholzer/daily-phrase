from dataclasses import dataclass
from pathlib import Path

from audio import CachedAudioPhrase

STATIC_ASSET_PATH = Path(__file__).parent / "static-assets/"


@dataclass
class LanguageInfo:
    """
    Representation of a language necessary to create a video.
    """

    country_name: str
    background_music_path: Path
    introduction_audio: CachedAudioPhrase


SPANISH = LanguageInfo(
    country_name="Spain",
    background_music_path=Path(
        "static-assets/music/sardana-by-kevin-macleod-from-filmmusic-io.mp3"
    ),
    introduction_audio=CachedAudioPhrase(
        native_phrase="Hello, and welcome to your daily Spanish lesson",
        foreign_phrase="Hola y bienvenido a tu clase diaria de español",
        native_audio_path=STATIC_ASSET_PATH
        / "introductions/spanish_introduction_english.mp3",
        foreign_audio_path=STATIC_ASSET_PATH
        / "introductions/spanish_introduction_spanish.mp3",
        native_audio_length=2.53,
        foreign_audio_length=4.49,
    ),
)
