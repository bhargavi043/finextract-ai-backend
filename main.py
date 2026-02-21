from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import pdfplumber
import pandas as pd
import os
from extractor import extract_financials
from utils import extract_years, detect_currency_unit

app = FastAPI(title="FinExtract AI")

@app.post("/extract")
async def extract(file: UploadFile = File(...)):

    text = ""

    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    years = extract_years(text)
    currency, unit = detect_currency_unit(text)

    structured_data = extract_financials(text)

    # Convert to DataFrame
    df = pd.DataFrame(structured_data).T
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Line Item"}, inplace=True)

    # Add metadata row
    metadata = pd.DataFrame({
        "Line Item": ["Currency", "Unit"],
        years[0] if years else "FY": [currency, unit]
    })

    output_file = "financial_output.csv"
    df.to_csv(output_file, index=False)

    return FileResponse(
        path=output_file,
        filename="financial_output.csv",
        media_type="text/csv"
    )