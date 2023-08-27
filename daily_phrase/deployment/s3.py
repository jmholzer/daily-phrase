import boto3
from pathlib import Path

BUCKET_NAME = "daily-phrase"


class S3VideoManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(S3VideoManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._s3_resource, self._s3_client = self._create_s3_session()

    def download_video_clip(self, native_language: str, foreign_language: str, video_path: Path) -> None:
        video_key = self._find_unpublished_video(native_language, foreign_language)
        if video_key is None:
            raise ValueError(
                f"No unpublished video with language pair ({native_language}, {foreign_language}) found."
            )
        self._s3_resource.Bucket(BUCKET_NAME).download_file(video_key, str(video_path))

    def _create_s3_session(self, profile="daily-phrase"):
        session = boto3.Session(profile_name=profile)
        s3_resource = session.resource("s3")
        s3_client = session.client('s3')
        return s3_resource, s3_client

    def _get_object_tags(self, object_key):
        response = self._s3_client.get_object_tagging(Bucket=BUCKET_NAME, Key=object_key)
        return response.get('TagSet', [])

    def _find_unpublished_video(self, native_language, foreign_language):
        bucket = self._s3_resource.Bucket(BUCKET_NAME)
        for obj in bucket.objects.all():
            tags = self._get_object_tags(obj.key)
            tag_data = {tag['Key']: tag['Value'] for tag in tags}
            if (
                tag_data.get('published') != "true" and
                tag_data.get('native_language') == native_language and
                tag_data.get('foreign_language') == foreign_language
            ):
                return obj.key
        return None
