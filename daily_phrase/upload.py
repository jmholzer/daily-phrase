import logging
from pathlib import Path

import boto3
from botocore.exceptions import NoCredentialsError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
from language import LanguagePair

BUCKET_NAME = "daily-phrase"
PROFILE_NAME = "daily-phrase"


def upload_to_s3(file_path: Path, language_pair: LanguagePair) -> None:
    """
    Uploads a file to an S3 bucket.

    :param file_name: Name of the file to be uploaded.
    :param bucket: Name of the S3 bucket.
    """
    session = boto3.Session(profile_name=PROFILE_NAME)
    s3 = session.client("s3")
    try:
        s3.upload_file(file_path, BUCKET_NAME, file_path.name)
        logger.info(f"Upload Successful for {file_path.name}")
        _tag_object(s3, file_path.name, language_pair)
        logger.info(f"Tag 'published=false' set for {file_path.name}")
    except FileNotFoundError:
        logger.info(f"The file {file_path} was not found")
    except NoCredentialsError:
        logger.info("Credentials not available")


def _tag_object(s3, object_key: str, language_pair: LanguagePair):
    s3.put_object_tagging(
        Bucket=BUCKET_NAME,
        Key=object_key,
        Tagging={
            "TagSet": [
                {"Key": "published", "Value": "false"},
                {"Key": "native_language", "Value": language_pair.native_language},
                {"Key": "foreign_language", "Value": language_pair.foreign_language},
            ]
        },
    )
