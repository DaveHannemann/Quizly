import whisper

model = whisper.load_model("turbo")

def transcribe_audio(path: str) -> str:
    result = model.transcribe(path)
    return result["text"]