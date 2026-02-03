from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.models import VoiceAnalysisRequest, VoiceAnalysisResponse, ErrorResponse
from app.services.gemini_service import gemini_service, SUPPORTED_LANGUAGES
from app.config import settings

router = APIRouter()

@router.post("/api/voice-detection", response_model=VoiceAnalysisResponse)
async def voice_detection(
    request: Request,
    body: VoiceAnalysisRequest
):
    """
    Analyze voice audio for AI_GENERATED vs HUMAN classification.
    Requires valid API key in x-api-key header.
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

    # Validate audio format is mp3
    if body.audioFormat.lower() != "mp3":
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Audio format must be mp3"
            }
        )

    # Validate audioBase64 is not empty
    if not body.audioBase64 or len(body.audioBase64.strip()) == 0:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "audioBase64 cannot be empty"
            }
        )

    # Call Gemini service
    result = gemini_service.analyze_audio(
        audio_base64=body.audioBase64,
        language=body.language
    )

    return VoiceAnalysisResponse(**result)