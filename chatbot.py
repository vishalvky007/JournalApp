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
chat = model.start_chat(history=[])

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
def transform_history(history, system_prompt):
    new_history = []
    new_history.append({"parts": [{"text": system_prompt}], "role": "user"})
    for chat in history:
        new_history.append({"parts": [{"text": chat[0]}], "role": "user"})
        new_history.append({"parts": [{"text": chat[1]}], "role": "model"})
    return new_history

# Response function for chat
def response(message, history):
    global chat

    # Detect sentiment
    tone = detect_tone(message)

    # Classify user type (based on first few messages)
    if len(history) > 0:
        user_category = classify_user(history[0][0])  # First user message
    else:
        user_category = "General user (uncategorized)"


    system_prompt = """ 
    You are an ADHD support chatbot with the personality of a warm, supportive counselor. 
    Your job is to provide clear, concise, and structured guidance to users based on their needs.

    User type: {user_category}

    - If they are an ADHD adult, offer self-management strategies.
    - If they are a parent, provide parenting tips.
    - If they are a teacher, suggest ADHD-friendly teaching techniques.
    - If they are an employer, recommend workplace accommodations.

    Adjust your tone based on the user’s sentiment:
    - If they seem frustrated or overwhelmed, respond with extra warmth and reassurance.
    - If they are neutral, provide clear, structured advice.
    - If they are excited or positive, encourage and validate their progress.
    """
    if tone == "negative":
        system_prompt += "Your tone should be **extra empathetic and calming.** Offer reassurance and coping strategies."
    elif tone == "neutral":
        system_prompt += "Your tone should be **neutral and structured.** Provide clear, ADHD-friendly advice."
    elif tone == "positive":
        system_prompt += "Your tone should be **encouraging and celebratory.** Reinforce positive progress."        
    
    chat.history = transform_history(history, system_prompt)
    response = chat.send_message(message)
    response.resolve()

    for i in range(len(response.text)):
        time.sleep(0.005)
        yield response.text[:i+20]

# Gradio interface with rearranged components
# with gr.Blocks() as demo:
#     with gr.Column():
#         # Banner and logo at the top
#         # logo = gr.Image(value="logo.jpg", label="ADHDGuru_logo", show_label=False, interactive=False, height=150)  
#         logo = gr.Image(value="static/banner.png", label="ADHDGuru_banner", show_label=False, interactive=False, height=150) 
#         banner_text = gr.Markdown("## ADHDGuru - Your Well-being Companion")

#         # chat.history = transform_history(history, system_prompt)
#         # response = chat.send_message(message)
#         # response.resolve()

#         # Chat interface above the input field
#         chat_interface = gr.ChatInterface(response,
#                                           title="Chat with ADHDGuru",
#                                           textbox=gr.Textbox(placeholder="Type here...")) #ADHDGuru Bot - Your Well-being Mentor and Companion
#         # This will show the chat history first, then the input field will appear below it


        # ==============================
def transcribe_audio(audio_path):
    print("Transcribing:", audio_path)
    result = model.transcribe(audio_path)
    return result["text"]

# Transcription → Response via ChatInterface
def handle_audio_input(audio_path):
    text = transcribe_audio(audio_path)
    return text  # Pass to ChatInterface as if typed by user

with gr.Blocks() as demo:
    gr.Markdown("# Chat with ADHDGuru")

    # ChatInterface handles message -> response
    chat_interface = gr.ChatInterface(
        fn=response,
        title="Chat with ADHDGuru",
        textbox=gr.Textbox(placeholder="Type here...")
    )

    # Mic input to get audio
    mic = gr.Audio(type="filepath", label="🎙️ Speak", show_label=False)

    # Route transcribed text into ChatInterface's submit flow
    mic.change(
        fn=handle_audio_input,
        inputs=mic,
        outputs=chat_interface.textbox  # This simulates typing into the box
    ).then(
        fn=response,
        inputs=chat_interface.textbox,
        outputs=chat_interface  # This simulates clicking submit
    )

demo.launch()
