from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

def analyze_note(note: str):
    prompt = f"""
You are an AI assistant.

Analyze this note.

Return ONLY valid JSON.

Example:

{{
  "summary": "...",
  "category": "...",
  "tags": ["...", "...", "..."]
}}

Note:

{note}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return json.loads(
        response.choices[0].message.content
    )