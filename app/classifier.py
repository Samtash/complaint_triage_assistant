import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.rules import CATEGORIES, URGENCIES

load_dotenv()

MODEL = "gemini-3.5-flash-lite"
_EXAMPLES = """
Examples:
Complaint: My replacement debit card has not arrived after three weeks.
JSON: {"category":"Cards","urgency":"Medium","reason":"The replacement card is delayed."}

Complaint: I cannot see yesterday's deposit in my account balance.
JSON: {"category":"Accounts","urgency":"Medium","reason":"A recent deposit is missing from the account balance."}

Complaint: The mobile banking app closes whenever I open the transfer page.
JSON: {"category":"Digital Banking","urgency":"Low","reason":"The app closes on the transfer page."}
""".strip()


def _parse_classification(response_text: str) -> dict[str, str]:
    result = json.loads(response_text)
    if not isinstance(result, dict) or set(result) != {"category", "urgency", "reason"}:
        raise ValueError("Gemini returned an unexpected JSON shape.")
    if result["category"] not in CATEGORIES or result["urgency"] not in URGENCIES:
        raise ValueError("Gemini returned an unsupported category or urgency.")
    if not isinstance(result["reason"], str) or not result["reason"].strip():
        raise ValueError("Gemini returned an empty reason.")
    return result


def classify_complaint(masked_text: str) -> dict[str, str] | None:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing from the environment or .env file.")

    client = genai.Client(api_key=api_key)
    prompt = f"""Classify this retail banking complaint.
Return only a JSON object with exactly these keys: category, urgency, reason.
category must be one of: {", ".join(CATEGORIES)}.
urgency must be one of: {", ".join(URGENCIES)}.
reason must be a short explanation. Do not add markdown or other text.

{_EXAMPLES}

Complaint: {masked_text}
"""

    for _ in range(2):
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
            ),
        )
        try:
            return _parse_classification(response.text or "")
        except (json.JSONDecodeError, TypeError, ValueError):
            continue
    return None