from elevenlabs import generate, save

from typing import Iterable, Dict
from pathlib import Path


TEMP_LOCATION = Path(__file__).parent.resolve() / Path("db/daily_phrase.db")


def _validate_api_key_set() -> None:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise Exception("Please set the ELEVENLABS_API_KEY environment variable")


def _generate_audio(tmp_path: Path, phrases: Iterable[Dict[str, str]]) -> None:
    for idx, phrase in enumerate(phrases):
        native_audio = generate(
            text=phrase["native_phrase"],
            model='eleven_multilingual_v1'
        )
        foreign_audio = generate(
            text=phrase["foreign_phrase"],
            model='eleven_multilingual_v1'
        )
        save(native_audio, str(tmp_path / f"native_audio_{idx}.mp3"))
        save(foreign_audio, str(tmp_path / f"foreign_audio_{idx}.mp3"))
