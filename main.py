import os
import base64
from fastapi import FastAPI, WebSocket
from fastapi.responses import PlainTextResponse, Response
from dotenv import load_dotenv
import uvicorn
import google.generativeai as genai
from twilio.rest import Client as TwilioClient
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings

# --- 1. CONFIGURATION ---
load_dotenv()

# Initialize API clients
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
twilio_client = TwilioClient(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
elevenlabs_voice_id = os.getenv("ELEVENLABS_VOICE_ID")

# Initialize FastAPI app
app = FastAPI()

# --- 2. GEMINI CONVERSATION SETUP ---
# We'll use a simple list to keep track of the conversation history
conversation_history = [
    {'role': 'user', 'parts': ["Let's have a brief conversation. Introduce yourself as a helpful AI assistant and ask me how you can help."]},
    {'role': 'model', 'parts': ["Hello! I'm a helpful AI assistant. How can I assist you today?"]}
]

gemini_model = genai.GenerativeModel('gemini-2.5-pro')
chat = gemini_model.start_chat(history=conversation_history)

@app.get("/")
async def root():
    """
    A simple endpoint to check if the server is running.
    """
    return {"message": "AI Voice Agent server is running successfully!"}

# --- 3. TWILIO WEBHOOKS ---
@app.post("/twilio/call", response_class=Response)
async def handle_twilio_call():
    """
    This endpoint is the first thing Twilio hits when a call is made.
    It returns TwiML instructions to start a WebSocket stream.
    """
    # Note: Replace 'YOUR_NGROK_URL' with your actual ngrok URL when you run it.
    # It will look something like 'wss://1a2b-3c4d-5e6f.ngrok.io/ws/call'
    # We will set this URL later. For now, this is a placeholder.
    twiml = """
    <Response>
        <Connect>
            <Stream url="wss://all-worms-occur.loca.lt/ws/call" />
        </Connect>
    </Response>
    """
    return Response(content=twiml, media_type="application/xml")


@app.websocket("/ws/call")
async def websocket_endpoint(websocket: WebSocket):
    """
    This is the main WebSocket endpoint that handles the real-time conversation.
    """
    await websocket.accept()
    print("WebSocket connection established.")

    try:
        while True:
            # Twilio sends messages as JSON strings
            message = await websocket.receive_text()
            
            # Here we would add logic to handle incoming audio, send it to STT,
            # then to Gemini, then to ElevenLabs TTS, and stream it back.
            # For this simplified POC, we'll just log the message.
            print(f"Received message from Twilio: {message}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("WebSocket connection closed.")

@app.get("/", response_class=PlainTextResponse)
async def home():
    return "AI Voice Agent server is running successfully!"


# --- 4. RUN THE APP ---
if __name__ == "__main__":
    print("Starting FastAPI server...")
    # NOTE: We'll run this from the command line using uvicorn instead.
    # uvicorn.run(app, host="0.0.0.0", port=8000)