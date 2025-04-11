import gradio as gr
import google.generativeai as genai
import time
from dotenv import load_dotenv
import os
import whisper
import tempfile
model = whisper.load_model("base")
# from journal import transcribe_audio
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load environment variables from .env file
load_dotenv()

# Get the Google API Key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
# genai.configure(api_key="")

# Initialize the chatbot model
model2 = genai.GenerativeModel('gemini-1.5-flash-latest')
chat = model2.start_chat(history=[])

# Initialize the sentiment analyzer
# analyzer = Sentim entIntensityAnalyzer()

# Function to detect user sentiment
def detect_tone(user_input):
    score = analyzer.polarity_scores(user_input)
    if score['compound'] >= 0.05:
        return "positive"
    elif score['compound'] <= -0.05:
        return "negative"
    else:
        return "neutral"

# Function to classify user type
def classify_user(user_input):
    user_input = user_input.lower()
    if "parent" in user_input:
        return "Parent of an ADHD child"
    elif "teacher" in user_input or "educator" in user_input:
        return "Teacher/Educator working with ADHD students"
    elif "employer" in user_input:
        return "Employer managing an ADHD employee"
    elif "adhd" in user_input or "adult" in user_input:
        return "Adult with ADHD"
    else:
        return "General user (uncategorized)"

# Function to transform Gradio history to Gemini format
class DummyChat:
    def __init__(self):
        self.history = []

    def send_message(self, message):
        class Response:
            def __init__(self, text):
                self.text = text
            def resolve(self):
                pass
        return Response(f"Processed: {message}")

chat = DummyChat()

# Your full response function
def response(message, history):
    global chat
    tone = detect_tone(message)

    if len(history) > 0:
        user_category = classify_user(history[0][0])
    else:
        user_category = "General user (uncategorized)"

    system_prompt = "Prompt based on tone. "
    if tone == "negative":
        system_prompt += "Your tone should be extra empathetic and calming."
    elif tone == "neutral":
        system_prompt += "Your tone should be neutral and structured."
    elif tone == "positive":
        system_prompt += "Your tone should be encouraging and celebratory."

    chat.history = transform_history(history, system_prompt)
    resp = chat.send_message(message)
    resp.resolve()

    for i in range(len(resp.text)):
        time.sleep(0.005)
        yield resp.text[:i+20]

# Whisper transcriber
def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]

# Only transcribe and return to textbox
def handle_audio_input(audio_path):
    return transcribe_audio(audio_path)

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# Chat with ADHDGuru")

    chat_interface = gr.ChatInterface(
        fn=response,
        title="Chat with ADHDGuru",
        chatbot=gr.Chatbot(),
        textbox=gr.Textbox(placeholder="Type here...")
    )

    mic = gr.Audio(type="filepath", label="🎙️ Speak", show_label=False)

    # Step 1: Transcribe → textbox
    mic.change(
        fn=handle_audio_input,
        inputs=mic,
        outputs=chat_interface.textbox
    ).then(
        # Step 2: Trigger submit with both message and history
        fn=chat_interface.fn,
        inputs=[chat_interface.textbox, chat_interface.chatbot],
        outputs=chat_interface.chatbot
    )

demo.launch()
