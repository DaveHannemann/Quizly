import yt_dlp
import tempfile
import os


def download_audio(url: str) -> str:
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_path = temp_file.name
    temp_file.close()

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": temp_path,
        "quiet": True,
        "noplaylist": True,
        }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


    final_path = temp_path + ".mp3"

    if not os.path.exists(final_path):
        raise Exception("Audio download failed")
    print("Audio downloaded to:", final_path)
    return final_path