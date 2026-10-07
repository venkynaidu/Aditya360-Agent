import os
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing. Create .env from .env.example.")
