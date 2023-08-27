from pathlib import Path

from metadata import get_video_metadata
from s3 import S3VideoManager
from youtube import YouTubeManager

VIDEO_PATH = Path(__file__).parent / "downloaded-videos"


def lambda_handler(event, context):
    native_langauge = event.get("native_language")
    foreign_language = event.get("foreign_language")
    youtube_channel_name = event.get("youtube_channel_name")
    video_metadata = get_video_metadata(native_langauge, foreign_language)

    try:
        video_manager = S3VideoManager()
        video_object_key = video_manager.download_video_clip(
            native_langauge, foreign_language, VIDEO_PATH
        )

        youtube_manager = YouTubeManager(youtube_channel_name)
        youtube_manager.upload_video_to_youtube(
            VIDEO_PATH / video_object_key, video_metadata
        )

        video_manager.set_video_published(video_object_key)
        return {"statusCode": 200, "body": "Function executed successfully"}
    except ValueError:
        return {"statusCode": 500, "body": "Function failed to execute"}
