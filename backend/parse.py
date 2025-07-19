import easyocr
from pdf2image import convert_from_path
import re
from .database import Receipt

# Predefined vendor categories
VENDOR_CATEGORIES = {
    "walmart": "Groceries",
    "amazon": "Shopping",
    "starbucks": "Food & Drink"
}

def extract_text(file_path):
    """Extract text using EasyOCR (no Tesseract needed)"""
    reader = easyocr.Reader(['en'])
    if file_path.lower().endswith('.pdf'):
        images = convert_from_path(file_path)
        results = reader.readtext(images[0])
    else:
        results = reader.readtext(file_path)
    return " ".join([text for (_, text, _) in results])

def parse_receipt(file_path):
    """Parse receipt text with simple rules"""
    text = extract_text(file_path).lower()
    
    # Find vendor
    vendor = next(
        (v for v in VENDOR_CATEGORIES if v in text),
        "unknown"
    ).title()

    # Find amount (looks for $xx.xx pattern)
    amount_match = re.search(r'total.*?(\d+\.\d{2})', text)
    amount = float(amount_match.group(1)) if amount_match else 0.0

    # Find date (common patterns)
    date_match = re.search(r'(\d{2}[/-]\d{2}[/-]\d{4})', text)
    date = date_match.group(1) if date_match else "unknown date"

    return Receipt(
        vendor=vendor,
        date=date,
        amount=amount,
        category=VENDOR_CATEGORIES.get(vendor.lower(), "Other")
    )