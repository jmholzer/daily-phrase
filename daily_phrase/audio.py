from elevenlabs import generate, save, Voice, VoiceSettings
from typing import Iterable, Dict, List, Union, Any
from pathlib import Path
from pydub.utils import mediainfo


TEMP_LOCATION = Path(__file__).parent.resolve() / Path("db/daily_phrase.db")
VOICE = Voice(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    name="Rachel",
    category="premade",
    settings=VoiceSettings(stability=0.75, similarity_boost=0.75),
)


def _create_audio(tmp_path: Path, phrases: List[Dict[str, Any]]) -> None:
    for idx in range(len(phrases)):
        phrases[idx]["native_audio_path"] = tmp_path / f"native_audio_{idx}.mp3"
        phrases[idx]["foreign_audio_path"] = tmp_path / f"foreign_audio_{idx}.mp3"
        _generate_and_save_audio(
            phrases[idx]["native_audio_path"], phrases[idx]["native_phrase"]
        )
        _generate_and_save_audio(
            phrases[idx]["foreign_audio_path"], phrases[idx]["foreign_audio_path"]
        )
        phrases[idx]["native_audio_length"] = _get_audio_length(
            phrases[idx]["native_audio_path"]
        )
        phrases[idx]["foreign_audio_length"] = _get_audio_length(
            phrases[idx]["foreign_audio_path"]
        )


def _generate_and_save_audio(output_path: Path, text: str) -> None:
    audio = generate(text=text, model="eleven_multilingual_v1", voice=VOICE)
    save(audio, output_path)


def _preprocess_prompts(phrases: Iterable[Dict[str, str]]) -> None:
    for phrase in phrases:
        phrase["foreign_phrase"] = phrase["foreign_phrase"].replace(" ", " - ")


def _get_audio_length(audio_path: Union[str, Path]) -> float:
    return mediainfo(str(audio_path))["duration"]
