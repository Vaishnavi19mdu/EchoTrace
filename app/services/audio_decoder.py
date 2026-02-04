# audio_decoder.py
import base64
import io
import tempfile
from typing import Tuple

import librosa
import numpy as np
from pydub import AudioSegment


def _load_with_librosa_bytestream(audio_bytes: bytes, sr=16000) -> Tuple[np.ndarray, int]:
    """
    Try to load audio from bytes into a waveform using librosa (audioread backend).
    """
    audio_buffer = io.BytesIO(audio_bytes)
    # librosa.load accepts a file-like object with audioread backend
    y, sr = librosa.load(audio_buffer, sr=sr, mono=True)
    return y, sr


def _load_with_pydub_and_librosa(audio_bytes: bytes, sr=16000, src_format="mp3"):
    """
    Fallback: write bytes to temp file, use pydub to convert to WAV, then load with librosa.
    This is more robust across formats (webm, mp3, etc.) if ffmpeg is available.
    """
    with tempfile.NamedTemporaryFile(suffix=f".{src_format}", delete=True) as tmp_in:
        tmp_in.write(audio_bytes)
        tmp_in.flush()
        # Load with pydub (requires ffmpeg)
        audio_seg = AudioSegment.from_file(tmp_in.name, format=src_format)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp_out:
            audio_seg.export(tmp_out.name, format="wav")
            y, sr = librosa.load(tmp_out.name, sr=sr, mono=True)
            return y, sr


def decode_base64_audio(audio_base64: str, audio_format: str = "mp3", sr: int = 16000):
    """
    Decode base64-encoded audio (mp3/webm) into a mono waveform at given sample-rate.

    Returns:
        waveform (np.ndarray), sr (int)
    Raises:
        ValueError on decode/load errors
    """
    if not audio_base64:
        raise ValueError("Empty audio_base64 provided")

    try:
        audio_bytes = base64.b64decode(audio_base64)
    except Exception as e:
        raise ValueError("Invalid base64 audio data") from e

    # Try librosa direct load from bytes
    try:
        return _load_with_librosa_bytestream(audio_bytes, sr=sr)
    except Exception:
        # fallback via pydub (more robust; requires ffmpeg)
        try:
            return _load_with_pydub_and_librosa(audio_bytes, sr=sr, src_format=audio_format)
        except Exception as e:
            raise ValueError("Could not decode audio. Ensure ffmpeg is installed for some formats.") from e
