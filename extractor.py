import json
import os
from openai import OpenAI

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

def extract_financials(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text[:15000]}
        ],
        temperature=0
    )

    content = response.choices[0].message.content
    return json.loads(content)