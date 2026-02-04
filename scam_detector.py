# scam_detector.py

SCAM_KEYWORDS = [
    "account blocked",
    "account suspended",
    "verify",
    "urgent",
    "upi",
    "otp",
    "click link",
    "bank",
    "freeze"
]

def is_scam(text: str) -> bool:
    text = text.lower()
    for keyword in SCAM_KEYWORDS:
        if keyword in text:
            return True
    return False
