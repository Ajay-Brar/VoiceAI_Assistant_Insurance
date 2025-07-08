import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
from dotenv import load_dotenv


load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TO_PHONE_NUMBER = os.getenv("TO_PHONE_NUMBER")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


app = FastAPI()
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Voice + Tone
voice_name = "Polly.Matthew"  # Professional male voice
voice_style = "<prosody pitch='-5%' rate='medium'>"  # Calm, serious tone

@app.get("/")
async def root():
    return {"message": "Insurance AI Assistant is running."}

@app.get("/call")
async def call():
    call = twilio_client.calls.create(
        to=TO_PHONE_NUMBER,
        from_=TWILIO_PHONE_NUMBER,
        url="https://1e9ab03e0625.ngrok-free.app/incoming-call" 
    )
    return {"message": f"Call initiated. Call SID: {call.sid}"}

@app.post("/incoming-call")
async def incoming_call(request: Request):
    response = VoiceResponse()
    gather = Gather(input="speech", action="/gather", method="POST", timeout=3, speechTimeout="auto")
    gather.say(
        f"<speak>{voice_style}Hello! This is John from SecureLife Insurance. "
        "We’re offering affordable plans for life, health, and vehicle coverage. "
        "Can I quickly tell you about one of our popular plans?</prosody></speak>",
        voice=voice_name, language="en-US"
    )
    response.append(gather)
    response.say(
        f"<speak>{voice_style}Hmm, I didn't hear anything. Call us anytime at SecureLife. Goodbye!</prosody></speak>",
        voice=voice_name, language="en-US"
    )
    return Response(content=str(response), media_type="application/xml")

@app.post("/gather")
async def gather(request: Request):
    form = await request.form()
    speech_result = form.get("SpeechResult", "")
    print(f"Caller said: {speech_result}")

    response = VoiceResponse()

    if not speech_result:
        response.say(
            f"<speak>{voice_style}Sorry, I didn't catch that. Could you repeat, please?</prosody></speak>",
            voice=voice_name, language="en-US"
        )
        gather = Gather(input="speech", action="/gather", method="POST", timeout=3, speechTimeout="auto")
        gather.say(
            f"<speak>{voice_style}Go ahead, I'm listening.</prosody></speak>",
            voice=voice_name, language="en-US"
        )
        response.append(gather)
        return Response(content=str(response), media_type="application/xml")

    # Hang up conditions
    if any(word in speech_result.lower() for word in ["no", "not interested", "stop", "bye", "exit"]):
        response.say(
            f"<speak>{voice_style}No worries! Thank you for your time. Stay safe and have a great day!</prosody></speak>",
            voice=voice_name, language="en-US"
        )
        response.hangup()
        return Response(content=str(response), media_type="application/xml")

    # Get reply from Groq
    ai_reply = get_groq_reply(speech_result)

    if len(ai_reply) > 400:
        ai_reply = ai_reply[:400] + "..."

    print(f"AI Assistant: {ai_reply}")
    reply_ssml = f"<speak>{voice_style}{ai_reply} <break time='500ms'/> Would you like me to send you a quote?</prosody></speak>"

    response.say(reply_ssml, voice=voice_name, language="en-US")
    gather = Gather(input="speech", action="/gather", method="POST", timeout=3, speechTimeout="auto")
    response.append(gather)

    return Response(content=str(response), media_type="application/xml")

def get_groq_reply(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are John, a warm, persuasive insurance sales assistant. "
                    "Your tone is helpful, professional, and human. "
                    "Explain benefits clearly and briefly—life, health, and vehicle insurance. "
                    "End with a friendly sales hook. Keep it under 50 words."
                )
            },
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        data = response.json()
        if "choices" not in data:
            print("Unexpected Groq API response:", data)
            return "We offer plans to protect your life, health, or car. They’re affordable and hassle-free. Want to hear more?"
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("Groq API error:", e)
        return "Our insurance plans are designed to give peace of mind. Let me know what you’re looking for."

