import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "").strip()

# Sarvam AI API Endpoints
SARVAM_BASE_URL = "https://api.sarvam.ai"
SARVAM_CHAT_URL = f"{SARVAM_BASE_URL}/v1/chat/completions"
SARVAM_TTS_URL = f"{SARVAM_BASE_URL}/text-to-speech"
SARVAM_TRANSLATE_URL = f"{SARVAM_BASE_URL}/translate"
SARVAM_DOC_URL = f"{SARVAM_BASE_URL}/doc-ai/v1/job/digitise"

# Preferred Sarvam Models
SARVAM_LLM_MODEL = os.getenv("SARVAM_LLM_MODEL", "sarvam-105b")
SARVAM_TTS_MODEL = "bulbul:v4-flash"
SARVAM_TRANSLATE_MODEL = "mayura:v1"

# Supported Regional Languages
LANGUAGE_MAP = {
    "en": {"code": "en-IN", "name": "English", "speaker": "meera"},
    "hi": {"code": "hi-IN", "name": "Hindi (हिन्दी)", "speaker": "meera"},
    "hinglish": {"code": "hi-IN", "name": "Hinglish (Colloquial)", "speaker": "arvind"},
    "te": {"code": "te-IN", "name": "Telugu (తెలుగు)", "speaker": "meera"},
    "ta": {"code": "ta-IN", "name": "Tamil (தமிழ்)", "speaker": "meera"},
}

# Database and App Configuration
if os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
    DB_PATH = Path("/tmp/samjhauta.db")
else:
    DB_PATH = Path(os.getenv("SQLITE_DB_PATH", str(BASE_DIR / "samjhauta.db")))

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
STATIC_DIR = BASE_DIR / "static"
