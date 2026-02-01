import json
import google.generativeai as genai
from app.config import settings

# Configure Gemini once
genai.configure(api_key=settings.GEMINI_API_KEY)

class GeminiService:
    def __init__(self):
        self.model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        self.mime_type_map = {
            "webm": "audio/webm",
            "mp3": "audio/mp3",
            "wav": "audio/wav",
            "ogg": "audio/ogg",
            "m4a": "audio/mp4"
        }
    
    def _get_prompt(self, language: str) -> str:
        """Generate the analysis prompt."""
        lang_context = (
            f"The expected language is {language}." 
            if language != "Auto" 
            else "Detect the language automatically."
        )
        
        return f"""Analyze this audio recording to determine if it's from a real human voice or AI-generated (text-to-speech, deepfake, etc.).

{lang_context}

Focus on:
1. Vocal authenticity - natural breath sounds, micro-variations in pitch
2. Prosody patterns - human-like rhythm and intonation changes
3. Spectral characteristics - frequency distributions typical of human vs synthetic voices
4. Artifacts - digital artifacts common in TTS/AI voices
5. Emotional authenticity - genuine emotional expression in voice

Respond ONLY in valid JSON format (no markdown):
{{
  "classification": "Human-generated" or "AI-generated",
  "confidence": <number 0.0 to 1.0>,
  "language": "English" or "Tamil" or "Hindi" or "Malayalam" or "Telugu" or "Unknown",
  "explanation": "Brief explanation of acoustic features that led to this classification"
}}"""
    
    def analyze_audio(self, audio_base64: str, audio_format: str, language: str) -> dict:
        """
        Analyze audio using Gemini.
        Returns dict with classification, confidence, language, explanation.
        Returns fallback "Unknown" response if parsing fails (Demo Safety Rule #11).
        """
        try:
            mime_type = self.mime_type_map.get(audio_format.lower(), "audio/webm")
            prompt = self._get_prompt(language)
            
            # Generate content
            result = self.model.generate_content([
                {
                    "mime_type": mime_type,
                    "data": audio_base64
                },
                prompt
            ])
            
            # Parse response
            response_text = result.text.strip()
            print(f"[Gemini Raw Response]: {response_text[:200]}")
            
            # Clean markdown if present
            response_text = response_text.replace("```json", "").replace("```", "").strip()
            
            # Try to parse JSON
            analysis = json.loads(response_text)
            
            # Validate required fields
            required_fields = ["classification", "confidence", "language", "explanation"]
            if not all(field in analysis for field in required_fields):
                raise ValueError("Missing required fields in Gemini response")
            
            return analysis
            
        except json.JSONDecodeError as e:
            print(f"[JSON Parse Error]: {e}")
            print(f"[Response Text]: {response_text}")
            return self._get_unknown_response("Invalid JSON from AI model")
        
        except Exception as e:
            print(f"[Gemini Service Error]: {str(e)}")
            return self._get_unknown_response(f"Analysis error: {str(e)[:50]}")
    
    def _get_unknown_response(self, reason: str) -> dict:
        """Fallback response for demo safety (PRD #11)."""
        return {
            "classification": "Unknown",
            "confidence": 0.0,
            "language": "Unknown",
            "explanation": f"Unable to analyze audio: {reason}"
        }

# Singleton instance
gemini_service = GeminiService()