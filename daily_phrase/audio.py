from dataclasses import dataclass
from pathlib import Path

from elevenlabs import Voice, VoiceSettings, generate, save
from pydub.utils import mediainfo

VOICE = Voice(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    name="Rachel",
    category="premade",
    settings=VoiceSettings(stability=1.0, similarity_boost=0.75),
)


@dataclass
class TMPAudioPhrase:
    """Represents a phrase with its native and foreign audio, and metadata."""

    media_dir: Path
    native_phrase: str
    foreign_phrase: str
    native_audio_path: Path | None = None
    foreign_audio_path: Path | None = None
    native_audio_length: float | None = None
    foreign_audio_length: float | None = None

    def __post_init__(self) -> None:
        """Preprocess the prompts and create the audio files."""
        self._preprocess_prompts()
        self._create_audio()

    def _preprocess_prompts(self) -> None:
        """Preprocess the foreign phrase by replacing spaces with dashes, causing the
        TTS to pause between words.
        """
        self.foreign_phrase = self.foreign_phrase.replace(" ", " - ")

    def _create_audio(self) -> None:
        """Create the audio files for the native and foreign phrases."""
        suffix = hash(self.native_phrase)
        self.native_audio_path = self.media_dir / f"native_audio_{suffix}.mp3"
        self.foreign_audio_path = self.media_dir / f"foreign_audio_{suffix}.mp3"
        self._create_audio_file(self.native_audio_path, self.native_phrase)
        self._create_audio_file(self.foreign_audio_path, self.foreign_phrase)
        self.native_audio_length = self._get_audio_length(self.native_audio_path)
        self.native_audio_length = self._get_audio_length(self.native_audio_path)

    @staticmethod
    def _create_audio_file(output_path: Path, text: str) -> None:
        """Generate an audio file from a text phrase using a specific voice model."""
        audio = generate(text=text, model="eleven_multilingual_v1", voice=VOICE)
        save(audio, output_path)

    @staticmethod
    def _get_audio_length(audio_path: str | Path) -> float:
        """Retrieve the duration of an audio file stored on disk."""
        return mediainfo(str(audio_path))["duration"]


@dataclass
class AudioPhrase:
    """Represents a phrase with its native and foreign audio, and metadata."""

    media_dir: Path
    native_phrase: str
    foreign_phrase: str
    native_audio_path: Path | None = None
    foreign_audio_path: Path | None = None
    native_audio_length: float | None = None
    foreign_audio_length: float | None = None
