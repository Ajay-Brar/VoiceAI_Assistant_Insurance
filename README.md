# VoiceAI_Insurance_Agent

🛡️ Insurance Voice AI Assistant – Powered by Twilio + Groq
This project is a voice-based AI sales assistant for insurance providers, built using FastAPI, Twilio, and Groq’s LLaMA 3. It makes outbound calls, 
speaks with human-like tone, and handles conversations in real time using voice recognition and AI-generated replies.

🎯 Features
📞 Auto-call customers using Twilio

🧠 Conversational AI powered by Groq (LLaMA3-8B)

🗣️ Amazon Polly voices with SSML prosody for tone control

🧾 Speaks about life, health, vehicle insurance

🛑 Handles user intent like "Not interested", "Tell me more", etc.

🌐 Built using FastAPI and deployed with ngrok or any server

🚀 How It Works
The app calls a customer using Twilio.

Customer hears a professional pitch (e.g., “We offer affordable life insurance…”).

They speak — their response is processed using Twilio's speech-to-text.

The AI (Groq LLaMA3) generates a human-like reply.

The assistant speaks back in a natural voice and asks follow-ups.

🧰 Technologies Used
Tech	Purpose
FastAPI	Backend API
Twilio	Outbound call + STT
Amazon Polly	Natural voice synthesis (e.g., Matthew)
Groq API	AI chatbot (LLaMA3 8B)
SSML	Speech tone + emotion control
Ngrok	Public HTTPS tunnel (for testing)
dotenv	Environment configuration

📁 Project Structure
.
├── main.py               # FastAPI app
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
├── static/               # Static files (if needed)
└── README.md             # Project documentation

💡 Customization
Change voice_name or voice_style in main.py for different tones

Update the system prompt in get_groq_reply() to change the AI’s personality

Add lead capture (to a database or Google Sheet)

Enable <Stream> + WebSocket for real-time processing

🛠️ Setup Instructions

1. Clone the Repo
terminal
git clone https://github.com/your-username/insurance-voice-ai.git
cd insurance-voice-ai

2. Install Dependencies
terminal
pip install -r requirements.txt

3. Create .env File
env

terminal
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1xxxxxxxxxx
TO_PHONE_NUMBER=+1xxxxxxxxxx
GROQ_API_KEY=your_groq_api_key

4. Run the FastAPI Server
terminal
uvicorn main:app --reload

5. Expose via Ngrok (For Twilio Callback)
terminal
ngrok http 8000
Replace the URL in the /call endpoint in main.py with your ngrok HTTPS URL, e.g.:
url="https://1234-56-78-90-123.ngrok-free.app/incoming-call"

6. Trigger a Call
Visit:
terminal
http://localhost:8000/call
