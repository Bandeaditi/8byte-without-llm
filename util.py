import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR"
from PIL import Image
import io
import re
from pdf2image import convert_from_bytes

def extract_fields(text):
    vendor = re.findall(r'(Amazon|Reliance|Flipkart|Airtel|Jio)', text)
    date = re.findall(r'\d{2}[/-]\d{2}[/-]\d{4}', text)
    amount = re.findall(r'Rs\.?\s?(\d+\.?\d*)', text)
    return {
        "vendor": vendor[0] if vendor else "Unknown",
        "date": date[0] if date else "Unknown",
        "amount": float(amount[0]) if amount else 0.0,
        "category": "General"
    }

def process_file(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        images = convert_from_bytes(uploaded_file.read())
        text = "".join([pytesseract.image_to_string(img) for img in images])
    else:
        image = Image.open(uploaded_file)
        text = pytesseract.image_to_string(image)

    return extract_fields(text)
