# guvi_callback.py

import requests

GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_guvi_callback(session_id: str, session: dict):
    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": session["message_count"],
        "extractedIntelligence": session["intelligence"],
        "agentNotes": "Scammer used urgency and payment redirection"
    }

    try:
        response = requests.post(
            GUVI_CALLBACK_URL,
            json=payload,
            timeout=5
        )
        return response.status_code
    except Exception as e:
        print("GUVI callback failed:", e)
        return None
