import os
import json

from .youtube_service import download_audio, validate_youtube_url, normalize_youtube_url
from .whisper_service import transcribe_audio
from .gemini_service import generate_quiz


def create_quiz(url: str):
    url = normalize_youtube_url(url)
    validate_youtube_url(url)

    audio_path = download_audio(url)

    try:
        transcript = transcribe_audio(audio_path)
        transcript = transcript[:5000]

        quiz_raw = generate_quiz(transcript)

        quiz_data = json.loads(quiz_raw)

        return quiz_data

    finally:
        os.remove(audio_path)