# daily-phrase

[![Python version](https://img.shields.io/badge/python-3.10-blue.svg)]
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/ambv/black)

Automatically generates short-form video content that teaches viewers a new phrase each day. Selects phrases from a pre-defined database, associates them with a relevant image, and combines audio and visuals into a learning video. These videos are then uploaded to an Amazon S3 bucket, from which an AWS Lambda function uploads them to  YouTube for distribution on a schedule.

See the [Spanish-Daily-Phrase YouTube channel](https://www.youtube.com/channel/UCTRL-ocjutuv_NLp6hHE0xA) for an example.

## Environment variables

export ELEVEN_API_KEY=...

export UNSPLASH_API_KEY=...

## Creating new phrases from JSON File

To create new phrase records in the db from a json file, whilst in the root of daily_phrase directory run:

```{bash}
python3 phrase.py --json cached_translations/<your_file>.json
```

## Upload

Created video files are stored in an S3 bucket. This is currently not configurable. Auth is currently handled using a profile (named `daily-phrase`) in the [AWS shared credentials file](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#shared-credentials-file).
