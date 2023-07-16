import requests
from pathlib import Path
import os


API_KEY = os.environ.get("UNSPLASH_API_KEY")


def _fetch_random_image_from_unsplash(country: str, tmp_dir: Path) -> None:
    image_url = _get_image_url(country)
    file_path = tmp_dir / f"{country}.jpg"
    _download_image(image_url, file_path)


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