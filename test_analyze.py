import requests
import base64

# Your API configuration
API_URL = "http://localhost:8000/analyze"
API_KEY = "cassiopieavoxp3"  # REPLACE THIS with your actual API_KEY from .env

# Create a tiny mock audio file (just for testing the API flow)
# This is a minimal WAV file header + silence
mock_audio_bytes = bytes([
    0x52, 0x49, 0x46, 0x46, 0x24, 0x00, 0x00, 0x00,
    0x57, 0x41, 0x56, 0x45, 0x66, 0x6d, 0x74, 0x20,
    0x10, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00,
    0x44, 0xac, 0x00, 0x00, 0x88, 0x58, 0x01, 0x00,
    0x02, 0x00, 0x10, 0x00, 0x64, 0x61, 0x74, 0x61,
    0x00, 0x00, 0x00, 0x00
])

# Convert to base64
audio_base64 = base64.b64encode(mock_audio_bytes).decode('utf-8')

# Prepare request
headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

payload = {
    "language": "Auto",
    "audioFormat": "wav",
    "audioBase64": audio_base64
}

print("🧪 Testing /analyze endpoint...")
print(f"API URL: {API_URL}")
print(f"API Key: {API_KEY}")
print("-" * 50)

try:
    response = requests.post(API_URL, json=payload, headers=headers)
    
    print(f"\n✅ Status Code: {response.status_code}")
    print(f"📄 Response:")
    print(response.json())
    
    if response.status_code == 200:
        print("\n🎉 SUCCESS! Your /analyze endpoint is working!")
        print("✅ Ready to share with frontend team")
    else:
        print(f"\n⚠️ Got status {response.status_code}")
        print("Check the error above")
        
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: Cannot connect to server")
    print("Make sure your server is running: python -m app.main")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")