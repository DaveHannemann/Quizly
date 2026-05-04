import os
import json

from .youtube_service import download_audio, validate_youtube_url, normalize_youtube_url
from .whisper_service import transcribe_audio
from .gemini_service import generate_quiz


def create_quiz(url: str):
    """
    End-to-end pipeline for generating a quiz from a YouTube video.

    Workflow:
        1. Normalize and validate the YouTube URL
        2. Download audio from the video
        3. Transcribe audio using Whisper
        4. Truncate transcript to a safe length (token limit handling)
        5. Generate quiz content using LLM (Gemini)
        6. Parse generated JSON into Python dict
        7. Clean up temporary audio file
    """
    
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