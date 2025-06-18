from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

app = FastAPI()

# CORS for frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/translate")
async def translate(request: Request):
    data = await request.json()
    input_text = data.get("text")
    target_languages = data.get("languages", [])  # List of language names like 'Hindi', 'Telugu'

    if not input_text or not target_languages:
        return {"error": "Missing 'text' or 'languages' field."}

    language_list = ", ".join(target_languages)
    prompt = f"Translate the following text into these languages ({language_list}):\n\n\"{input_text}\""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GEMINI_URL, json=payload)
        return response.json()