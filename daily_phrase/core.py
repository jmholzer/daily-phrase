
from pathlib import Path
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip

from typing import List, Dict, Any


def _create_video_from_image(video_length: float, tmp_dir: Path) -> None:
    image_path = next(tmp_dir.glob("*.jpg"))  # Get the first jpg image in tmp/
    clip = ImageClip(str(image_path), duration=video_length)
    clip_resized = clip.resize(height=1920, width=1080)
    clip_resized.write_videofile(tmp_dir / "video.mp4", codec='libx264')


def _add_audio_to_video(phrases: List[Dict[str, Any]], video_path: Path) -> None:
    pass


def _add_text_overlay(video_path: Path, text: str, start_time: float) -> None:
    video = ImageClip(str(video_path))
    txt_clip = (TextClip(text, fontsize=70, color='white')
                .set_position(('center', 'bottom'))
                .set_start(start_time)
                .set_duration(video.duration - start_time))

    result = CompositeVideoClip([video, txt_clip])
    result.write_videofile(f"{video_path.parent}/{video_path.stem}_overlay.mp4", codec='libx264')
