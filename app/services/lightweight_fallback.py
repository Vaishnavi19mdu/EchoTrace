import base64
import math
from collections import Counter

def lightweight_audio_features(audio_base64: str) -> dict:
    raw = base64.b64decode(audio_base64)

    size = len(raw)
    counts = Counter(raw)

    entropy = -sum(
        (c / size) * math.log2(c / size)
        for c in counts.values()
    )

    return {
        "pitch_variance": min(0.3, entropy / 10),
        "rhythm_variance": min(0.3, size / 1_000_000),
        "pause_ratio": max(0.02, entropy / 12),
        "spectral_smoothness": min(0.95, 1 - entropy / 15)
    }
