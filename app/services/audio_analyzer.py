from .audio_decoder import decode_base64_audio
from .feature_extractor import extract_voice_features
from .language_handler import validate_language
from .temporal_analyzer import pitch_temporal_consistency


def analyze_audio(audio_base64: str, language: str, audio_format: str = "mp3"):
    """
    Main audio analysis entry point.

    Returns:
    {
        "language": <validated language>,
        "features": { ... }
    }
    """

    # Validate language (no guessing)
    lang = validate_language(language)

    # Decode audio
    y, sr = decode_base64_audio(audio_base64, audio_format)

    # Extract base features
    features = extract_voice_features(y, sr)

    # Temporal pitch consistency
    features["pitch_consistency"] = pitch_temporal_consistency(y, sr)

    return {
        "language": lang,
        "features": features
    }
