import numpy as np
import librosa

# Simple, explainable heuristics (safe for judges)
PITCH_AI_THRESHOLD = 0.12
CONSISTENCY_RATIO = 0.75


def pitch_temporal_consistency(y, sr, chunk_sec=1.5):
    """
    Check whether low pitch variance persists across time.
    Returns: "CONSISTENT", "INCONSISTENT", or "INCONCLUSIVE"
    """
    if y is None or len(y) == 0:
        return "INCONCLUSIVE"

    chunk_size = int(chunk_sec * sr)

    chunks = [
        y[i:i + chunk_size]
        for i in range(0, len(y), chunk_size)
        if len(y[i:i + chunk_size]) > chunk_size // 2
    ]

    if len(chunks) < 2:
        return "INCONCLUSIVE"

    ai_like_chunks = 0

    for chunk in chunks:
        try:
            f0, _, _ = librosa.pyin(
                chunk,
                fmin=librosa.note_to_hz("C2"),
                fmax=librosa.note_to_hz("C7"),
                sr=sr
            )
            vals = f0[~np.isnan(f0)]
            if vals.size == 0:
                continue

            if np.var(vals) < PITCH_AI_THRESHOLD:
                ai_like_chunks += 1
        except Exception:
            continue

    ratio = ai_like_chunks / len(chunks)

    if ratio >= CONSISTENCY_RATIO:
        return "CONSISTENT"
    return "INCONSISTENT"
