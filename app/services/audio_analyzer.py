from .audio_decoder import decode_base64_audio
from .feature_extractor import extract_voice_features
from .language_handler import validate_language
from .temporal_analyzer import pitch_temporal_consistency
from .lightweight_fallback import lightweight_audio_features


def analyze_audio(audio_base64: str, language: str, audio_format: str = "mp3"):
    lang = validate_language(language)

    y, sr = decode_base64_audio(audio_base64, audio_format)

    # ✅ CASE 1: Real waveform available
    if y is not None:
        features = extract_voice_features(y, sr)
        features["pitch_consistency"] = pitch_temporal_consistency(y, sr)

    # ✅ CASE 2: Decoder unavailable → byte-level inference
    else:
        features = lightweight_audio_features(audio_base64)

    return {
        "language": lang,
        "features": features
    }
