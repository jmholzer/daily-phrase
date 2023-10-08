# daily-phrase

Automatically generates short-form video content that teaches viewers a new phrase each day

## Environment variables

export ELEVEN_API_KEY=...

export UNSPLASH_API_KEY=...

## Creating new phrases from JSON File

To create new phrase records in the db from a json file, whilst in the root of daily_phrase directory run:

```{bash}
python3 phrase.py --json cached_translations/<your_file>.json
```

## Upload

Created video files are stored in an S3 bucket. This is currently not configurable. Authorisation is currently handled using a profile (named `daily-phrase`) in the [AWS shared credentials file](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#shared-credentials-file).
