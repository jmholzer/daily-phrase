import os
from pathlib import Path

import requests

API_KEY = os.environ.get("UNSPLASH_API_KEY")


def download_random_image_from_unsplash(country_name: str, tmp_dir: Path) -> Path:
    file_path = tmp_dir / f"{country_name}.jpg"
    _download_image(country_name, file_path)
    return file_path


def _download_image(country_name: str, file_path: Path) -> str:
    url = (
        f"https://source.unsplash.com/random/1080x1920?{country_name}"
    )
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
