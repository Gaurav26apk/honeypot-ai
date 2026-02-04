# intelligence_extractor.py

import re

def extract_intelligence(text: str, intelligence: dict):
    # Phone numbers (Indian)
    phones = re.findall(r"\b(?:\+91[- ]?)?[6-9]\d{9}\b", text)
    intelligence["phoneNumbers"].extend(phones)

    # UPI IDs
    upi_ids = re.findall(r"\b[\w.\-]{2,}@[a-zA-Z]{2,}\b", text)
    intelligence["upiIds"].extend(upi_ids)

    # URLs
    urls = re.findall(r"https?://\S+", text)
    intelligence["phishingLinks"].extend(urls)

    # Keywords
    keywords = ["urgent", "verify", "blocked", "otp", "upi", "bank"]
    for kw in keywords:
        if kw in text.lower():
            intelligence["suspiciousKeywords"].append(kw)
