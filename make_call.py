import os
from dotenv import load_dotenv
from twilio.rest import Client

# --- CONFIGURATION ---
load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(account_sid, auth_token)

# --- IMPORTANT: UPDATE THESE VALUES ---
# Your personal Indian mobile number in E.164 format
your_phone_number = "+919618160545" 

# Your ngrok forwarding URL (the https one)
ngrok_url = "https://ai-caller-poc-36.onrender.com" 
# ------------------------------------

print(f"📞 Initiating call from {twilio_number} to {your_phone_number}...")

try:
    call = client.calls.create(
        url=f"{ngrok_url}/twilio/call",
        to=your_phone_number,
        from_=twilio_number
    )
    print(f"✅ Call initiated successfully! SID: {call.sid}")
except Exception as e:
    print(f"❌ Error initiating call: {e}")