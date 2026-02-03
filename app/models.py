from pydantic import BaseModel

class VoiceAnalysisRequest(BaseModel):
    language: str  # Tamil / English / Hindi / Malayalam / Telugu
    audioFormat: str  # Always mp3
    audioBase64: str  # Base64-encoded MP3 audio

class VoiceAnalysisResponse(BaseModel):
    status: str  # "success"
    language: str  # Tamil / English / Hindi / Malayalam / Telugu
    classification: str  # AI_GENERATED / HUMAN
    confidenceScore: float  # 0.0 to 1.0
    explanation: str  # Short reason for the decision

class ErrorResponse(BaseModel):
    status: str  # "error"
    message: str  # Error message