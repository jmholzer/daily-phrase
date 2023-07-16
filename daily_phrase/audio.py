from elevenlabs import generate, save, Voice, VoiceSettings
from typing import Iterable, Dict
from pathlib import Path


TEMP_LOCATION = Path(__file__).parent.resolve() / Path("db/daily_phrase.db")
VOICE = Voice(
    voice_id='21m00Tcm4TlvDq8ikWAM',
    name='Rachel',
    category='premade',
    settings=VoiceSettings(stability=0.75, similarity_boost=0.75)
)


def _create_audio(tmp_path: Path, phrases: Iterable[Dict[str, str]]) -> None:
    for idx, phrase in enumerate(phrases):
        native_audio = generate(
            text=phrase["native_phrase"], model="eleven_multilingual_v1",
            voice=VOICE
        )
        foreign_audio = generate(
            text=phrase["foreign_phrase"], model="eleven_multilingual_v1",
            voice=VOICE
        )
        save(native_audio, str(tmp_path / f"native_audio_{idx}.mp3"))
        save(foreign_audio, str(tmp_path / f"foreign_audio_{idx}.mp3"))


def _preprocess_prompts(phrases: Iterable[Dict[str, str]]) -> None:
    for phrase in phrases:
        phrase["foreign_phrase"] = (
            phrase["foreign_phrase"].replace(" ", " - ")
        )
