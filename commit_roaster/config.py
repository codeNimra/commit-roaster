"""Configuration for Commit Roaster."""

import os
from dotenv import load_dotenv
load_dotenv()
from google.generativeai import GenerativeModel

# Load from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set in .env file")

# Initialize Gemini
def get_gemini_model():
    """Returns configured Gemini model."""
    return GenerativeModel(GEMINI_MODEL, api_key=GEMINI_API_KEY)

MAX_COMMITS = 10  # Default roasts per repo
