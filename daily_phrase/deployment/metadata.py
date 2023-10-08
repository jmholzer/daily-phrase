from .utils import generate_title_formatted_date


class Metadata:
    channel_name: str = None
    title: str = None
    description: str = None
    language_tag: str = None


class EnglishSpanishMetadata(Metadata):
    channel_name: str = "daily-phrase"
    title: str = (
        f"Daily Spanish Phrases 🇪🇸🇲🇽 {generate_title_formatted_date()} #LearnSpanish"
    )
    description: str = (
        "Master the Spanish language one phrase at a time!\n"
        "Subscribe for daily Spanish lessons! #SpanishPhrases #LearnSpanishFast #Shorts\n"
        "Music: Sardana by Kevin MacLeod\n"
        "Free download: https://filmmusic.io/song/5002-sardana\n"
        "Licensed under CC BY 4.0: https://filmmusic.io/standard-license"
    )
    language_tag: str = "Spanish"


def get_video_metadata(native_language, foreign_language):
    if f"{native_language.upper()}_{foreign_language.upper()}" == "ENGLISH_SPANISH":
        return EnglishSpanishMetadata
    else:
        raise ValueError("Unsupported language combination.")
