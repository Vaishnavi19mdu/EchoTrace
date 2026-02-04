# language_handler.py

SUPPORTED = {
    "tamil": "Tamil",
    "english": "English",
    "hindi": "Hindi",
    "malayalam": "Malayalam",
    "telugu": "Telugu",
    # Accept "auto" as a special value — we do NOT infer language from audio.
    "auto": "Auto"
}


def validate_language(lang: str) -> str:
    """
    Validate and normalize language input.
    Accepts exact names (case-insensitive) or 'Auto'.
    Returns canonical form (e.g., "Tamil") or "Auto".
    Raises ValueError if unsupported.
    """
    if not lang:
        raise ValueError("Language field is required")

    key = lang.strip().lower()
    if key not in SUPPORTED:
        raise ValueError(f"Unsupported language '{lang}'. Allowed: {list(set(SUPPORTED.values()))}")
    return SUPPORTED[key]
