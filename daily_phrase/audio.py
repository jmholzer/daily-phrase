from elevenlabs import generate, save, Voice, VoiceSettings
from pathlib import Path
from pydub.utils import mediainfo
from dataclasses import dataclass


TEMP_LOCATION = Path(__file__).parent.resolve() / Path("db/daily_phrase.db")
VOICE = Voice(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    name="Rachel",
    category="premade",
    settings=VoiceSettings(stability=0.75, similarity_boost=0.75),
)


@dataclass
class AudioPhrase:
    """Represents a phrase with its native and foreign audio, and metadata.
    """

    native_phrase: str
    foreign_phrase: str
    native_audio_path: Path | None = None
    foreign_audio_path: Path | None = None
    native_audio_length: float | None = None
    foreign_audio_length: float | None = None

    def preprocess_prompts(self) -> None:
        """Preprocess the foreign phrase by replacing spaces with dashes, causing the
        TTS to pause between words.
        """
        self.foreign_phrase = self.foreign_phrase.replace(" ", " - ")

    def create_audio(self, tmp_path: Path) -> None:
        """Create the audio files for the native and foreign phrases.
        """
        suffix = hash(self.native_phrase)
        self.native_audio_path = tmp_path / f"native_audio_{suffix}.mp3"
        self.foreign_audio_path = tmp_path / f"foreign_audio_{suffix}.mp3"
        self._create_audio_file(self.native_audio_path, self.native_phrase)
        self._create_audio_file(self.foreign_audio_path, self.foreign_phrase)
        self.native_audio_length = self._get_audio_length(self.native_audio_path)
        self.native_audio_length = self._get_audio_length(self.native_audio_path)

    @staticmethod
    def _create_audio_file(output_path: Path, text: str) -> None:
        """Generate an audio file from a text phrase using a specific voice model.
        """
        audio = generate(text=text, model="eleven_multilingual_v1", voice=VOICE)
        save(audio, output_path)

    @staticmethod
    def _get_audio_length(audio_path: str | Path) -> float:
        """Retrieve the duration of an audio file stored on disk.
        """
        return mediainfo(str(audio_path))["duration"]


def create_audio_files(tmp_path: Path, audio_phrases: list[AudioPhrase]) -> None:
    """Process a list of AudioPhrase instances by preprocessing their prompts and
    creating their audio files.
    """
    for audio_phrase in audio_phrases:
        audio_phrase.preprocess_prompts()
        audio_phrase.create_audio(tmp_path)
