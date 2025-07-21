import os
import easyocr
import pandas as pd
import re
from difflib import get_close_matches

# Set your image folder name
image_folder = "images"

# Predefined known vendor names (add more if you want)
KNOWN_VENDORS = ["Amazon", "Flipkart", "Reliance", "Airtel", "Jio", "Paytm", "Big Bazaar"]

reader = easyocr.Reader(['en'])

def extract_text_from_image(image_path):
    try:
        result = reader.readtext(image_path, detail=0)
        return " ".join(result)
    except:
        return ""

def extract_vendor(text):
    for line in text.split("\n"):
        match = get_close_matches(line.strip(), KNOWN_VENDORS, n=1, cutoff=0.7)
        if match:
            return match[0]
    return "Unknown"

def extract_date(text):
    match = re.search(r'\d{2}[/-]\d{2}[/-]\d{4}', text)
    return match.group(0) if match else "Unknown"

def extract_amount(text):
    text = text.replace(",", "")
    matches = re.findall(r'\d{2,7}(?:\.\d{1,2})?', text)
    return max([float(x) for x in matches], default=0.0)

# Go through all image files
data = []
for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.pdf')):
        path = os.path.join(image_folder, filename)
        print(f"📄 Processing {filename}...")
        ocr_text = extract_text_from_image(path)
        vendor = extract_vendor(ocr_text)
        date = extract_date(ocr_text)
        amount = extract_amount(ocr_text)
        data.append({
            "filename": filename,
            "vendor": vendor,
            "date": date,
            "amount": amount,
            "ocr_text": ocr_text
        })

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("receipts.csv", index=False)
print("✅ Done! Saved to receipts.csv")
