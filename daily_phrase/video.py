from pathlib import Path

from moviepy.editor import (
    AudioFileClip,
    ColorClip,
    CompositeVideoClip,
    CompositeAudioClip,
    ImageClip,
    TextClip,
)

from audio import AudioPhrase

PAUSE_LENGTH = 0.5
BG_MUSIC_FADEOUT_LENGTH = 3
BG_MUSIC_VOLUME = 0.15
TEXT_SIZE = (800, 300)
TEXT_FONT_SIZE = 70


class Video:
    def __init__(
        self, image_path: Path, audio_phrases: list[AudioPhrase], tmp_media_dir: Path, bg_music: Path
    ) -> None:
        self._image_path = image_path
        self._audio_phrases = audio_phrases
        self._audio_timings = []
        self._video_length = 0
        self._tmp_dir = tmp_media_dir
        self._bg_music = bg_music

        self._calculate_audio_start_times()
        self._create_video_from_image()
        self._add_text_overlay()
        self._add_audio_to_video()
        self._save_video_file()

    def _calculate_audio_start_times(self) -> None:
        t = 0  # Start at 0 seconds
        for phrase in self._audio_phrases:
            self._audio_timings.append((phrase, t))
            t += phrase.native_audio_length + phrase.foreign_audio_length * 2 + 2
        self._video_length = t + BG_MUSIC_FADEOUT_LENGTH

    def _create_video_from_image(self) -> None:
        print(f"self._image_path: {self._image_path}")
        self._video = ImageClip(
            str(self._image_path), duration=self._video_length
        ).resize(height=1920, width=1080)

    def _add_audio_to_video(self) -> None:
        audio_clips = []
        bg_music_clip = (
            AudioFileClip(str(self._bg_music))
            .subclip(0, self._video_length)
            .audio_fadeout(BG_MUSIC_FADEOUT_LENGTH)
            .volumex(BG_MUSIC_VOLUME)
        )
        audio_clips.append(bg_music_clip)

        for phrase, start_time in self._audio_timings:
            audio_clips.append(
                AudioFileClip(str(phrase.native_audio_path)).set_start(start_time)
            )
            start_time += phrase.native_audio_length + PAUSE_LENGTH
            audio_clips.append(
                AudioFileClip(str(phrase.foreign_audio_path)).set_start(start_time)
            )
            start_time += phrase.foreign_audio_length + PAUSE_LENGTH
            audio_clips.append(
                AudioFileClip(str(phrase.foreign_audio_path)).set_start(start_time)
            )
        self._video = self._video.set_audio(CompositeAudioClip(audio_clips))

    def _add_text_overlay(self) -> None:
        text_clips = []
        for phrase, start_time in self._audio_timings:
            # Create the text clips
            native_text_clip = self._create_text_clip(
                phrase.native_phrase, phrase.native_audio_length, start_time
            )
            start_time += phrase.native_audio_length + PAUSE_LENGTH
            foreign_text_clip = self._create_text_clip(
                phrase.foreign_phrase, phrase.foreign_audio_length * 2 + PAUSE_LENGTH, start_time
            )
            text_clips.extend([native_text_clip, foreign_text_clip])
        # Overlay the text-background composites onto the video
        self._video = CompositeVideoClip([self._video] + text_clips)

    def _create_text_clip(
        self, text: str, length: float, start_time: float
    ) -> CompositeVideoClip:
        native_text = (
            TextClip(
                text, fontsize=TEXT_FONT_SIZE, color="white", method="caption", size=TEXT_SIZE
            )
            .set_duration(length)
            .set_start(start_time)
        )
        # Create a black background that fits the text
        background = (
            ColorClip(size=native_text.size, color=(0, 0, 0))
            .set_duration(length)
            .set_start(start_time)
        )
        # Overlay the text over the background
        return CompositeVideoClip([background, native_text]).set_position(
            ("center", "center")
        )

    def _save_video_file(self) -> None:
        self._video.write_videofile(
            str(self._tmp_dir / "video.mp4"),
            codec="libx264",
            fps=60,
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
        )
