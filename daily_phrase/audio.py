from dataclasses import dataclass, field
from pathlib import Path

from elevenlabs import Voice, VoiceSettings, generate, save
from pydub.utils import mediainfo

VOICE = Voice(
    voice_id="XB0fDUnXU5powFXDhCwa",
    name="Charlotte",
    category="premade",
    settings=VoiceSettings(stability=1.0, similarity_boost=0.75),
)


@dataclass
class AudioPhrase:
    """Represents a phrase with its native and foreign audio, and metadata."""

    media_dir: Path
    native_phrase: str
    foreign_phrase: str
    native_audio_path: Path = field(init=False)
    foreign_audio_path: Path = field(init=False)
    native_audio_length: float = field(init=False)
    foreign_audio_length: float = field(init=False)

    def __post_init__(self) -> None:
        """Preprocess the prompts and create the audio files."""
        self._create_audio()

    def _preprocess_prompt(self, phrase: str) -> str:
        """Preprocess the foreign phrase by replacing spaces with dashes, causing the
        TTS to pause between words.
        """
        return phrase.replace(" ", " - ")

    def _create_audio(self) -> None:
        """Create the audio files for the native and foreign phrases."""
        suffix = abs(hash(self.native_phrase))
        self.native_audio_path = self.media_dir / f"native_audio_{suffix}.mp3"
        self.foreign_audio_path = self.media_dir / f"foreign_audio_{suffix}.mp3"
        self._create_audio_file(self.native_audio_path, self.native_phrase)
        self._create_audio_file(
            self.foreign_audio_path, self._preprocess_prompt(self.foreign_phrase)
        )
        self.native_audio_length = self._get_audio_length(self.native_audio_path)
        self.foreign_audio_length = self._get_audio_length(self.foreign_audio_path)

    @staticmethod
    def _create_audio_file(output_path: Path, text: str) -> None:
        """Generate an audio file from a text phrase using a specific voice model."""
        audio = generate(text=text, model="eleven_multilingual_v1", voice=VOICE)
        save(audio, output_path)

    @staticmethod
    def _get_audio_length(audio_path: str | Path) -> float:
        """Retrieve the duration of an audio file stored on disk."""
        return float(mediainfo(str(audio_path))["duration"])


@dataclass
class CachedAudioPhrase:
    """Represents a phrase with its native and foreign audio, and metadata."""

    native_phrase: str
    foreign_phrase: str
    native_audio_path: Path
    foreign_audio_path: Path
    native_audio_length: float
    foreign_audio_length: float
