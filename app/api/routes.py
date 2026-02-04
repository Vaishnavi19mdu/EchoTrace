from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.models import VoiceAnalysisRequest, VoiceAnalysisResponse
from app.services.integrated_service import integrated_service
from app.config import settings

router = APIRouter()

SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

@router.post("/api/voice-detection", response_model=VoiceAnalysisResponse)
async def voice_detection(
    request: Request,
    body: VoiceAnalysisRequest
):
    """
    Integrated EchoTrace Detection
    Person 2 (audio) → Person 1 (classification) → Person 3 (API)
    """
    # Validate API key
    api_key = request.headers.get("x-api-key")
    if not api_key or api_key != settings.API_KEY:
        return JSONResponse(
            status_code=401,
            content={
                "status": "error",
                "message": "Invalid API key or malformed request"
            }
        )

    # Validate language
    if body.language not in SUPPORTED_LANGUAGES:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": f"Unsupported language. Use one of: {', '.join(SUPPORTED_LANGUAGES)}"
            }
        )

    # Validate audio format
    if body.audioFormat.lower() != "mp3":
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Audio format must be mp3"
            }
        )

    # Validate audioBase64 not empty
    if not body.audioBase64 or len(body.audioBase64.strip()) == 0:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "audioBase64 cannot be empty"
            }
        )

    # Call integrated service (Person 2 → Person 1)
    result = integrated_service.analyze_audio_integrated(
        audio_base64=body.audioBase64,
        language=body.language,
        audio_format=body.audioFormat
    )

    return VoiceAnalysisResponse(**result)
