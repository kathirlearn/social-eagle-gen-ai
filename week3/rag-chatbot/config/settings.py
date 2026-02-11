import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY missing in .env")

if not SERPAPI_API_KEY:
    raise ValueError("❌ SERPAPI_API_KEY missing in .env")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 4
SIMILARITY_THRESHOLD = 0.35
