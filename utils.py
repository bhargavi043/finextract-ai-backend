import re

def extract_years(text):
    years = re.findall(r'FY\s?\d{2}', text)
    return sorted(list(set(years)))

def detect_currency_unit(text):
    currency = "UNKNOWN"
    unit = "UNKNOWN"

    if "₹" in text or "INR" in text:
        currency = "INR"
    elif "USD" in text:
        currency = "USD"

    if "crore" in text.lower():
        unit = "Crores"
    elif "lakh" in text.lower():
        unit = "Lakhs"
    elif "million" in text.lower():
        unit = "Millions"

    return currency, unit

def clean_number(value):
    try:
        value = value.replace(",", "")
        return float(value)
    except:
        return None