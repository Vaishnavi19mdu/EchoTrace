# audio_decoder.py
import base64
import io
import warnings

# Silence ffmpeg / avconv warnings (local dev only)
warnings.filterwarnings("ignore", category=RuntimeWarning)

from pydub import AudioSegment
import librosa
import numpy as np


def decode_base64_audio(audio_base64: str, audio_format: str = "mp3"):
    """
    Decodes Base64 audio into waveform + sample rate.

    Works on:
    - Render / production (ffmpeg available)
    - Local dev (imports won't crash; decoding may fail gracefully)

    Returns:
        y (np.ndarray): audio waveform
        sr (int): sample rate

    Raises:
        ValueError: if decoding fails or input is invalid
    """
    if not audio_base64:
        raise ValueError("Empty audio input")

    try:
        # Decode base64 → bytes
        audio_bytes = base64.b64decode(audio_base64)

        # Bytes → audio segment
        audio_file = io.BytesIO(audio_bytes)
        audio = AudioSegment.from_file(audio_file, format=audio_format)

        # Convert to mono
        audio = audio.set_channels(1)

        # Convert to numpy array
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)

        # Normalize to [-1.0, 1.0]
        samples /= np.iinfo(audio.array_type).max

        # Sample rate
        sr = audio.frame_rate

        # Ensure librosa compatibility
        y = librosa.util.normalize(samples)

        return y, sr

    except Exception as e:
        raise ValueError(
            "Audio decoding failed. "
            "This is expected in local dev without ffmpeg. "
            "Use deployed service for full analysis."
        ) from e
