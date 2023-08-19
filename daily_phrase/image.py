import os
from pathlib import Path

import requests

API_KEY = os.environ.get("UNSPLASH_API_KEY")


def download_random_image_from_unsplash(country_name: str, tmp_dir: Path) -> Path:
    image_url = _get_image_url(country_name)
    file_path = tmp_dir / f"{country_name}.jpg"
    _download_image(image_url, file_path)
    return file_path


def _get_image_url(country: str) -> str:
    url = (
        f"https://api.unsplash.com/photos/random?query={country}"
        f"&client_id={API_KEY}&orientation=portrait"
    )
    response = requests.get(url)
    response.raise_for_status()
    image_url = response.json()["urls"]["full"]
    return image_url


def _download_image(image_url: str, file_path: Path) -> None:
    response = requests.get(image_url, stream=True)
    response.raise_for_status()
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
