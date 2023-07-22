from pathlib import Path
from audio import AudioPhrase
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip


class Video:

    def __init__(self, image_path: Path, audio_phrases: list[AudioPhrase], tmp_media_dir: Path) -> None:
        self._image_path = image_path
        self._audio_phrases = audio_phrases
        self._audio_timings = {}
        self._tmp_dir = tmp_media_dir

        self._calculate_audio_start_times()
        self._create_video_from_image()
        self._add_audio_to_video()
        self._save_video_file()

    def _calculate_audio_start_times(self) -> None:
        t = 0  # Start at 0 seconds
        for phrase in self._audio_phrases:
            t += phrase.native_audio_length + phrase.foreign_audio_length + 2
            self._audio_timings[phrase] = t

    def _create_video_from_image(self) -> None:
        video_length = sum(self._audio_timings.values())
        self._video = (
            ImageClip(str(self._image_path), duration=video_length)
            .resize(height=1920, width=1080)
        )

    def _add_audio_to_video(self) -> None:
        for phrase, start_time in self._audio_timings.items():
            audio_clip = concatenate_videoclips([
                AudioFileClip(str(phrase.native_audio_path)),
                AudioFileClip(str(phrase.foreign_audio_path))
            ]).set_start(start_time)
            audio_clip = AudioFileClip(str(phrase.native_audio_path)).set_start(start_time)
            self._video.set_audio(audio_clip)

    def _add_text_overlay(self, video_path: Path, text: str, start_time: float) -> None:
        # TODO: Finish
        video = ImageClip(str(video_path))
        txt_clip = (
            TextClip(text, fontsize=70, color='white')
            .set_position(('center', 'bottom'))
            .set_start(start_time)
            .set_duration()
        )
        result = CompositeVideoClip([video, txt_clip])
        result.write_videofile(f"{video_path.parent}/{video_path.stem}_overlay.mp4", codec='libx264')

    def _save_video_file(self) -> None:
        self._video.write_videofile(self._tmp_dir / "video.mp4", codec='libx264')
