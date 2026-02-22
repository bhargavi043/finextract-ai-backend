import json
import os
import re
from openai import OpenAI
from openai import RateLimitError, AuthenticationError

# Initialize OpenAI client using environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a financial analyst.
Extract ONLY income statement line items from the provided text.

Rules:
- Return STRICT JSON
- Do NOT invent numbers
- If missing, write null
- Extract all fiscal years
- Use exact numbers from text
- Do NOT include explanations
- Output ONLY valid JSON

Format:
{
  "Revenue from Operations": {"FY25": 12345, "FY24": 10000},
  "Other Income": {...},
  "Total Revenue": {...},
  "EBITDA": {...},
  "Depreciation": {...},
  "Finance Cost": {...},
  "Profit Before Tax": {...},
  "Tax Expense": {...},
  "Profit After Tax": {...}
}
"""


def clean_json_response(content: str):
    """
    Remove markdown formatting and clean JSON before parsing.
    """
    if content.startswith("```"):
        content = re.sub(r"```json|```", "", content).strip()
    return content


def extract_financials(text: str):
    try:
        if not text or not text.strip():
            raise ValueError("Empty document text")

        # Prevent token overflow
        trimmed_text = text[:15000]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": trimmed_text}
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        content = clean_json_response(content)

        return json.loads(content)

    except AuthenticationError:
        print("ERROR: Invalid or missing OpenAI API key.")
        return {"error": "Invalid API key"}

    except RateLimitError:
        print("ERROR: OpenAI quota exceeded.")
        return {"error": "OpenAI quota exceeded. Please check billing."}

    except json.JSONDecodeError:
        print("ERROR: OpenAI returned invalid JSON.")
        return {"error": "Model returned invalid JSON format"}

    except Exception as e:
        print("Unexpected error:", str(e))
        return {"error": str(e)}