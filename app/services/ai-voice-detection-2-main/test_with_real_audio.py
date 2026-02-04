# test_with_real_audio.py
import argparse
import base64
import json
import sys

from audio_analyzer import analyze_audio


def mp3_file_to_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def main():
    parser = argparse.ArgumentParser(description="Test Person-2 audio analyzer with a real MP3")
    parser.add_argument("--file", "-f", required=True, help="Path to local MP3 file")
    parser.add_argument("--language", "-l", required=True, help="Language label to send (Tamil/English/Hindi/Malayalam/Telugu/Auto)")
    parser.add_argument("--format", default="mp3", help="audio format (mp3 or webm) - for decoder fallback")
    args = parser.parse_args()

    try:
        audio_b64 = mp3_file_to_base64(args.file)
    except Exception as e:
        print("Could not open audio file:", e, file=sys.stderr)
        sys.exit(2)

    try:
        result = analyze_audio(audio_b64, language=args.language, audio_format=args.format)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print("Error analyzing audio:", str(e), file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
