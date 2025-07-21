import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import re
import os
from difflib import get_close_matches

# -------------------- SETUP --------------------
reader = easyocr.Reader(['en'], verbose=False)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------- FUNCTIONS --------------------
def extract_vendor(text):
    lines = text.splitlines()
    top_lines = lines[:5]
    candidates = []
    for line in top_lines:
        line = line.strip()
        if len(line) >= 3 and line.isupper() and not line.isnumeric():
            candidates.append(line)
    if candidates:
        return candidates[0]
    for line in top_lines:
        if line.strip():
            return line.strip()
    return "Unknown"

def extract_date(text):
    match = re.search(r'\d{2}[/-]\d{2}[/-]\d{4}', text)
    return match.group(0) if match else "Unknown"

def extract_amount(text):
    text = text.lower().replace(",", "")
    lines = text.split("\n")
    keywords = ["total", "subtotal", "grand total", "amount", "total amount"]
    candidates = []
    for line in lines:
        if any(k in line for k in keywords):
            matches = re.findall(r'\d{2,7}(?:\.\d{1,2})?', line)
            candidates += [float(m) for m in matches]
    if candidates:
        return max(candidates)
    matches = re.findall(r'\d{2,7}(?:\.\d{1,2})?', text)
    return max([float(m) for m in matches], default=0.0)

def detect_currency(text):
    text = text.lower()
    if "₹" in text or "rs" in text:
        return "INR ₹"
    elif "$" in text:
        return "USD $"
    elif "€" in text:
        return "EUR €"
    elif "£" in text:
        return "GBP £"
    return "Unknown"

def ocr_and_extract(image):
    img_array = np.array(image)
    result = reader.readtext(img_array, detail=0)
    full_text = "\n".join(result)
    return {
        "ocr_text": full_text,
        "vendor": extract_vendor(full_text),
        "date": extract_date(full_text),
        "amount": extract_amount(full_text),
        "currency": detect_currency(full_text)
    }

# -------------------- UI --------------------
st.set_page_config(page_title="🧾 Receipt Analyzer", layout="centered")
st.title("🧾 Upload and Analyze Receipt")

uploaded_file = st.file_uploader("Upload receipt image (.jpg, .png, .jpeg)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Receipt", use_column_width=True)

    with st.spinner("Analyzing receipt..."):
        result = ocr_and_extract(image)

    vendor = st.text_input("🛍️ Vendor", result["vendor"])
    date = st.text_input("📅 Date", result["date"])
    amount = st.number_input("💰 Amount", value=result["amount"])
    currency = result["currency"]
    ocr_text = result["ocr_text"]

    with st.expander("📌 Receipt Summary"):
        st.markdown(f"""
        - 🏷️ **Vendor**: `{vendor}`  
        - 🗓️ **Date**: `{date}`  
        - 💲 **Amount**: `{amount}`  
        - 💱 **Currency**: `{currency}`  
        - 📄 **Lines Detected**: `{len(ocr_text.splitlines())}`
        """)

    with st.expander("📃 Full OCR Text"):
        st.text_area("OCR Output", ocr_text, height=200)
