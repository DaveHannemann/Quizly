import yt_dlp
import tempfile
import os
from urllib.parse import urlparse, parse_qs


def download_audio(url: str) -> str:
    temp_dir = tempfile.mkdtemp()

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(temp_dir, "%(id)s.%(ext)s"),
        "quiet": True,
        "noplaylist": True,
        "js_runtimes": {
            "node": {}
        },
        }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)



    if not os.path.exists(file_path):
        raise Exception("Audio download failed")
    
    return file_path

def validate_youtube_url(url: str):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=False)
    except Exception:
        raise ValueError("Unknown YouTube-URL")

def normalize_youtube_url(url: str) -> str:
    parsed = urlparse(url)

    if "youtube.com" in parsed.netloc:
        query = parse_qs(parsed.query)
        video_id = query.get("v")
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id[0]}"

    if "youtu.be" in parsed.netloc:
        video_id = parsed.path.lstrip("/")
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"

    raise ValueError("Unknown YouTube-URL")