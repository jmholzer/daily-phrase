
from pathlib import Path


from audio import AudioPhrase


from image import download_random_image_from_unsplash
from tempfile import TemporaryDirectory


def main(country: str) -> None:
    """Main entry point for the daily_phrase package.
    """
    audio_phrases = _load_phrases()  # TODO: implement this function
    with TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)
        download_random_image_from_unsplash(country, tmp_dir)
        _create_video_from_image(video_length=5.0, tmp_dir=tmp_dir)


def _load_phrases() -> list[AudioPhrase]:
    pass
