import re
from difflib import get_close_matches

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
