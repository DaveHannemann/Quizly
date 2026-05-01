import yt_dlp
import tempfile
import os


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
    
    print("Audio downloaded to:", file_path)
    return file_path