
from pathlib import Path
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip

from audio import AudioPhrase


from image import download_random_image_from_unsplash
from tempfile import TemporaryDirectory


def main(country: str) -> None:
    """Main entry point for the daily_phrase package.
    """
    audio_phrases = _load_phrases()  # TODO: implement this function
    with TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)
        _create_audio_files(tmp_dir, audio_phrases)
        download_random_image_from_unsplash(country, tmp_dir)
        _create_video_from_image(video_length=5.0, tmp_dir=tmp_dir)


def _load_phrases() -> list[AudioPhrase]:
    pass


def _create_audio_files(tmp_path: Path, audio_phrases: list[AudioPhrase]) -> None:
    """Process a list of AudioPhrase instances by preprocessing their prompts and
    creating their audio files.
    """
    for audio_phrase in audio_phrases:
        audio_phrase.preprocess_prompts()
        audio_phrase.create_audio(tmp_path)


def _create_video_from_image(video_length: float, tmp_dir: Path) -> None:
    image_path = next(tmp_dir.glob("*.jpg"))  # Get the first jpg image in tmp/
    clip = ImageClip(str(image_path), duration=video_length)
    clip_resized = clip.resize(height=1920, width=1080)
    clip_resized.write_videofile(tmp_dir / "video.mp4", codec='libx264')


def _add_audio_to_video(phrases: list[AudioPhrase], video_path: Path) -> None:
    pass


def _add_text_overlay(video_path: Path, text: str, start_time: float) -> None:
    video = ImageClip(str(video_path))
    txt_clip = (TextClip(text, fontsize=70, color='white')
                .set_position(('center', 'bottom'))
                .set_start(start_time)
                .set_duration(video.duration - start_time))

    result = CompositeVideoClip([video, txt_clip])
    result.write_videofile(f"{video_path.parent}/{video_path.stem}_overlay.mp4", codec='libx264')
