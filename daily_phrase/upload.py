import boto3
from botocore.exceptions import NoCredentialsError
import logging
from pathlib import Path
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


BUCKET_NAME = "daily-phrase"


def upload_to_s3(file_path: Path) -> None:
    """
    Uploads a file to an S3 bucket.

    :param file_name: Name of the file to be uploaded.
    :param bucket: Name of the S3 bucket.
    """
    # Initialize S3 client
    s3 = boto3.client('s3', profile_name='daily-phrase')
    try:
        # Upload file to the specified S3 bucket
        s3.upload_file(file_path, BUCKET_NAME, file_path.name)
        logger.info(f"Upload Successful for {file_path.name}")
        # Set 'published' tag to false
        s3.put_object_tagging(
            Bucket=BUCKET_NAME,
            Key=file_path.name,
            Tagging={
                'TagSet': [
                    {
                        'Key': 'published',
                        'Value': 'false'
                    }
                ]
            }
        )
        logger.info(f"Tag 'published=false' set for {file_path.name}")
    except FileNotFoundError:
        logger.info(f"The file {file_path} was not found")
    except NoCredentialsError:
        logger.info("Credentials not available")
