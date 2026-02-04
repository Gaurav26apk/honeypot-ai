# agent_controller.py

def generate_reply(text: str, message_count: int) -> str:
    text = text.lower()

    if "bank" in text:
        return "Which bank is this? I have accounts in multiple banks."

    if "upi" in text:
        return "I am not sure where to find my UPI ID. Can you guide me?"

    if "otp" in text:
        return "I received many messages today. Which OTP are you asking about?"

    if message_count < 3:
        return "I am worried. Can you please explain clearly?"

    return "I am trying to understand. What should I do now?"
