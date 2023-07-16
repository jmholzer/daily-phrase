import requests
from pathlib import Path
import os
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip


API_KEY = os.environ.get("UNSPLASH_API_KEY")


def _create_video_from_image(video_length: float, tmp_dir: Path) -> None:
    image_path = next(tmp_dir.rglob("*.jpg"))  # Get the first jpg image in tmp/
    clip = ImageClip(str(image_path), duration=video_length)
    clip_resized = clip.resize(height=1920, width=1080)
    clip_resized.write_videofile(tmp_dir / "video.mp4", codec='libx264')


def _add_text_overlay(video_path: Path, text: str, start_time: float) -> None:
    video = ImageClip(str(video_path))
    txt_clip = (TextClip(text, fontsize=70, color='white')
                .set_position(('center', 'bottom'))
                .set_start(start_time)
                .set_duration(video.duration - start_time))

    result = CompositeVideoClip([video, txt_clip])
    result.write_videofile(f"{video_path.parent}/{video_path.stem}_overlay.mp4", codec='libx264')


def _fetch_random_image_from_unsplash(country: str, tmp_dir: Path) -> None:
    image_url = _get_image_url(country)
    file_path = tmp_dir / f"{country}.jpg"
    _download_image(image_url, file_path)


def _get_image_url(country: str) -> str:
    url = (
        f"https://api.unsplash.com/photos/random?query={country}"
        f"&client_id={API_KEY}&orientation=portrait"
    )
    response = requests.get(url)
    response.raise_for_status()
    image_url = response.json()["urls"]["full"]
    return image_url


def _download_image(image_url: str, file_path: Path) -> None:
    response = requests.get(image_url, stream=True)
    response.raise_for_status()
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
