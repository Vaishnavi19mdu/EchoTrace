import pytest
from app.services.gemini_service import GeminiService

def test_unknown_response_format():
    """Test that fallback response has correct structure."""
    service = GeminiService()
    result = service._get_unknown_response("Test error")
    
    assert result["classification"] == "Unknown"
    assert result["confidence"] == 0.0
    assert result["language"] == "Unknown"
    assert "Test error" in result["explanation"]

def test_prompt_generation():
    """Test prompt includes language context."""
    service = GeminiService()
    
    prompt_auto = service._get_prompt("Auto")
    assert "Detect the language automatically" in prompt_auto
    
    prompt_tamil = service._get_prompt("Tamil")
    assert "The expected language is Tamil" in prompt_tamil