# feature_extractor.py
import numpy as np
import librosa


def extract_voice_features(y: np.ndarray, sr: int):
    """
    Extracts a small set of explainable acoustic features used by the decision engine:
      - pitch_variance (variance of estimated F0 across voiced frames)
      - rhythm_variance (variance of onset strength envelope)
      - pause_ratio (fraction of short-time frames below RMS threshold)
      - spectral_smoothness (normalized smoothness metric derived from MFCC diffs)
      - duration_seconds

    Returns: dict of features (floats)
    """
    if y is None or len(y) == 0:
        raise ValueError("Empty waveform provided")

    duration_sec = len(y) / float(sr)

    # 1) Pitch (F0) variance using librosa.pyin (works on voiced speech)
    try:
        f0, voiced_flag, voiced_probs = librosa.pyin(
            y,
            fmin=librosa.note_to_hz("C2"),
            fmax=librosa.note_to_hz("C7"),
            sr=sr
        )
        # f0 can contain np.nan for unvoiced frames
        pitch_vals = f0[~np.isnan(f0)]
        pitch_variance = float(np.var(pitch_vals)) if pitch_vals.size > 0 else 0.0
    except Exception:
        # fallback: use zero as unreliable
        pitch_variance = 0.0

    # 2) Rhythm variance (onset strength variance)
    try:
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        rhythm_variance = float(np.var(onset_env)) if onset_env.size > 0 else 0.0
    except Exception:
        rhythm_variance = 0.0

    # 3) Pause ratio (frames with very low RMS energy)
    try:
        rms = librosa.feature.rms(y=y)[0]  # shape (n_frames,)
        silence_frames = rms < 0.01  # threshold; empirical
        pause_ratio = float(np.sum(silence_frames) / rms.size) if rms.size > 0 else 0.0
    except Exception:
        pause_ratio = 0.0

    # 4) Spectral smoothness - normalized metric (0..1), higher ~ smoother
    try:
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        # Frame-to-frame mean absolute diff
        diffs = np.mean(np.abs(np.diff(mfcc, axis=1)), axis=0)
        mean_diff = np.mean(diffs) if diffs.size > 0 else 0.0
        mean_mfcc = np.mean(np.abs(mfcc)) + 1e-9
        # Normalize: smaller mean_diff relative to MFCC magnitude -> smoother
        raw = 1.0 - (mean_diff / mean_mfcc)
        spectral_smoothness = float(np.clip(raw, 0.0, 1.0))
    except Exception:
        spectral_smoothness = 0.0

    # Round and return
    return {
        "duration_seconds": round(float(duration_sec), 3),
        "pitch_variance": round(float(pitch_variance), 6),
        "rhythm_variance": round(float(rhythm_variance), 6),
        "pause_ratio": round(float(pause_ratio), 6),
        "spectral_smoothness": round(float(spectral_smoothness), 6)
    }
