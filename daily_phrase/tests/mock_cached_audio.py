from pathlib import Path

from daily_phrase.audio import CachedAudioPhrase

STORED_MEDIA_PATH = Path(__file__).parent / "media/"


def _mock_load_phrases() -> list[CachedAudioPhrase]:
    return [
        CachedAudioPhrase(
            "I'm looking for a good book to read.",
            "Estoy buscando un buen libro para leer.",
            native_audio_path=STORED_MEDIA_PATH
            / "native_audio_-917148876481730440.mp3",
            native_audio_length=1.93,
            foreign_audio_path=STORED_MEDIA_PATH
            / "foreign_audio_-917148876481730440.mp3",
            foreign_audio_length=3.11,
        ),
        CachedAudioPhrase(
            "I need to talk to you about something important.",
            "Necesito hablar contigo acerca de algo importante.",
            native_audio_path=STORED_MEDIA_PATH
            / "native_audio_1365006673279825515.mp3",
            native_audio_length=2.32,
            foreign_audio_path=STORED_MEDIA_PATH
            / "foreign_audio_1365006673279825515.mp3",
            foreign_audio_length=3.94,
        ),
    ]
