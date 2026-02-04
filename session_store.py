# session_store.py

sessions = {}

def get_session(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = {
            "conversation": [],
            "message_count": 0,
            "scam_detected": False,
            "completed": False,
            "callback_sent": False,
            "intelligence": {
                "bankAccounts": [],
                "upiIds": [],
                "phishingLinks": [],
                "phoneNumbers": [],
                "suspiciousKeywords": []
            }
        }
    return sessions[session_id]
