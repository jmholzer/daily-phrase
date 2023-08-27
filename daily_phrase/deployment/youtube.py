from pathlib import Path
import json

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

EDUCATION_CATEGORY_ID = "27"


class YouTubeManager:

    _instance = None

    def __new__(cls, channel_name):
        if cls._instance is None:
            cls._instance = super(YouTubeManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, channel_name):
        self._channel_name = channel_name
        self.youtube = self._get_authenticated_service()

    def upload_video_to_youtube(self, file_path):
        body = {
            "snippet": {
                "title": "Test video #short",
                "description": "Uploaded video",
                "tags": ["sample", "example"],
                "categoryId": EDUCATION_CATEGORY_ID,
            },
            "status": {"privacyStatus": "private"},
        }
        media = MediaFileUpload(file_path, mimetype="video/mp4", resumable=True)

        try:
            request = self.youtube.videos().insert(
                part=",".join(body.keys()), body=body, media_body=media
            )
            response = request.execute()
            return response
        except HttpError as e:
            print(f"An error occurred: {e}")
            raise ValueError("Failed to upload the video to YouTube.")

    def _get_authenticated_service(self):
        oauth2_info_path = Path(__file__).parent / f"credentials/{self._channel_name}-oauth2-info.json"

        with open(oauth2_info_path, "r") as file:
            oauth2_info = json.load(file)

        credentials = Credentials(
            token=None,
            refresh_token=oauth2_info["refresh_token"],
            client_id=oauth2_info["client_id"],
            client_secret=oauth2_info["client_secret"],
            token_uri='https://oauth2.googleapis.com/token'
        )

        return build("youtube", "v3", credentials=credentials)
