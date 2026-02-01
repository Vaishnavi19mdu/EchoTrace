from fastapi import APIRouter, HTTPException, Header
from app.models import VoiceAnalysisRequest, VoiceAnalysisResponse
from app.services.gemini_service import gemini_service
from app.config import settings

router = APIRouter()

@router.post("/analyze", response_model=VoiceAnalysisResponse)
async def analyze_voice(
    request: VoiceAnalysisRequest,
    x_api_key: str = Header(None)
):
    """
    Analyze voice audio for Human vs AI classification.
    Requires valid API key in x-api-key header.
    """
    # Validate API key
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Call Gemini service
    analysis = gemini_service.analyze_audio(
        audio_base64=request.audioBase64,
        audio_format=request.audioFormat,
        language=request.language
    )
    
    return VoiceAnalysisResponse(**analysis)