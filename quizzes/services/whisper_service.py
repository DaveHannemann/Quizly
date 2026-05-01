import whisper

model = None

def get_model():
    global model
    if model is None:
        model = whisper.load_model("base")
    return model

def transcribe_audio(path: str) -> str:
    model = get_model()
    result = model.transcribe(path)
    return result["text"]