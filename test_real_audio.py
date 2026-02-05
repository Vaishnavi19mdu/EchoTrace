import requests
import base64
import json

# Read the sample MP3 file and convert to base64
with open("app/services/sample_voice_1.mp3", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode("utf-8")

# API endpoint
url = "https://projwhitehat.onrender.com/api/voice-detection"

# Headers
headers = {
    "x-api-key": "cassiopeiavoxp3",
    "Content-Type": "application/json"
}

# Request body
data = {
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": audio_base64
}

# Make request
response = requests.post(url, headers=headers, json=data)

print(json.dumps(response.json(), indent=2))