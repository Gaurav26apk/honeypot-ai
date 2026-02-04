from fastapi import FastAPI, Header, HTTPException, Request
from dotenv import load_dotenv
import os

from session_store import get_session
from scam_detector import is_scam
from agent_controller import generate_reply
from intelligence_extractor import extract_intelligence
from guvi_callback import send_guvi_callback

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Honeypot API is live"
    }

@app.post("/api/honeypot/message")
async def receive_message(
    request: Request,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # 🔹 STEP 1: Read raw body safely
    body = await request.body()

    # 🔹 STEP 2: If NO BODY → this is GUVI endpoint tester
    if not body or body.strip() == b"":
        return {
            "status": "success",
            "message": "Honeypot API reachable and authenticated"
        }

    # 🔹 STEP 3: Now it's SAFE to parse JSON
    try:
        data = await request.json()
    except:
        return {
            "status": "error",
            "message": "Invalid JSON body"
        }

    session_id = data.get("sessionId")
    message = data.get("message")

    if not session_id or not message:
        return {
            "status": "error",
            "message": "Invalid request body"
        }

    session = get_session(session_id)

    text = message.get("text", "")

    if not session["scam_detected"]:
        if is_scam(text):
            session["scam_detected"] = True

    extract_intelligence(text, session["intelligence"])

    session["conversation"].append(message)
    session["message_count"] += 1

    intel = session["intelligence"]
    has_intel = (
        len(intel["upiIds"]) > 0 or
        len(intel["phoneNumbers"]) > 0 or
        len(intel["phishingLinks"]) > 0
    )

    if session["scam_detected"] and (
        session["message_count"] >= 10 or has_intel
    ):
        session["completed"] = True

        if not session["callback_sent"]:
            send_guvi_callback(session_id, session)
            session["callback_sent"] = True

        return {
            "status": "success",
            "reply": "Thank you, I will check and get back.",
            "conversationCompleted": True
        }

    reply = generate_reply(text, session["message_count"]) if session["scam_detected"] else "Okay."

    return {
        "status": "success",
        "scamDetected": session["scam_detected"],
        "reply": reply,
        "messageCount": session["message_count"]
    }
