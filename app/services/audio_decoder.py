def decode_base64_audio(audio_base64: str, audio_format: str = "mp3", sr: int = 16000):
    """
    Decode base64 audio into waveform.
    If decoding fails (no ffmpeg), return None instead of crashing.
    """
    if not audio_base64:
        raise ValueError("Empty audio_base64 provided")

    try:
        audio_bytes = base64.b64decode(audio_base64)
    except Exception as e:
        raise ValueError("Invalid base64 audio data") from e

    # Try librosa byte stream
    try:
        return _load_with_librosa_bytestream(audio_bytes, sr=sr)
    except Exception:
        # Try pydub only if ffmpeg exists
        try:
            return _load_with_pydub_and_librosa(audio_bytes, sr=sr, src_format=audio_format)
        except Exception:
            # ❗ IMPORTANT: graceful degradation
            return None, None
