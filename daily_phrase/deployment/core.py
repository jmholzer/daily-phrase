from s3 import S3VideoManager
from youtube import YouTubeManager

from pathlib import Path


VIDEO_PATH = Path(__file__).parent / "video.mp4"


def lambda_handler(event, context):
    native_langauge = event.get("native_language")
    foreign_language = event.get("foreign_language")
    youtube_channel_name = event.get("youtube_channel_name")

    try:
        video_manager = S3VideoManager()
        video_manager.download_video_clip(native_langauge, foreign_language, VIDEO_PATH)

        youtube_manager = YouTubeManager(youtube_channel_name)
        youtube_manager.upload_video_to_youtube(VIDEO_PATH)

        return {
            'statusCode': 200,
            'body': 'Function executed successfully'
        }
    except ValueError:
        return {
            'statusCode': 500,
            'body': 'Function failed to execute'
        }
