from pydantic import BaseModel

class VoiceAnalysisRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

class VoiceAnalysisResponse(BaseModel):
    classification: str
    confidence: float
    language: str
    explanation: str