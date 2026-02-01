import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_KEY: str = os.getenv("API_KEY", "your-secret-api-key-here")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    
    # Validate required keys
    @classmethod
    def validate(cls):
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

settings = Settings()
settings.validate()