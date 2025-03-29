import streamlit as st
import whisper
import tempfile
model = whisper.load_model("base")
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
from prompts import JOURNAL_PROMPT
API = os.environ['GROQ_API']
llm = ChatGroq(model="gemma2-9b-it", api_key=API)

def transcribe_audio(audio_file):

    current_directory = os.path.dirname(os.path.abspath(__file__))
    temp_file_path = os.path.join(current_directory, "temp_audio.wav")

    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(audio_file.read())
        temp_file.flush()
    print("---------------", temp_file_path)
    result = model.transcribe(temp_file_path)
    return result['text'] 





st.write("Please speak or upload the audio")
speak = st.checkbox('Speak')
upload = st.checkbox('Upload')

# Display the checkbox values
if speak:
    audio_value = st.audio_input("Record a voice message")
    if audio_value:
        st.audio(audio_value)

if upload:
    audio_file = st.file_uploader("Upload Audio File", type=["mp3", "wav", "ogg"])
    if audio_file is not None:
        st.audio(audio_file)
        
        if st.button("Convert to Journal"):
            with st.spinner("Converting the Audio..."):
#                 transcription = """ Woke up late today, way past my alarm. Felt groggy, probably should sleep earlier. Checked my phone first thing—bad habit, I know. Emails, messages, some news, nothing exciting. Had a quick breakfast, just coffee and a slice of bread, then straight to work.

# Spent way too long on a stupid bug in my AI model. Thought it was a major issue, turns out I just missed a small config change. Annoying but at least it’s fixed. Had a meeting after that, mostly about optimizing data pipelines. Some parts were interesting, but honestly, I was zoning out halfway through. Too much theory, not enough action.

# Lunch was whatever, just a sandwich. I should start cooking real meals. Afternoon was a blur, some coding, some scrolling, not as productive as I wanted. Went for a run in the evening, which helped clear my head. Caught up with a few friends later, random conversations about tech, life, and stupid things from college.

# Now just lying in bed, feeling kind of exhausted but also like I didn’t do enough. Some progress, but nothing major. Maybe tomorrow will be better."""
                transcription = transcribe_audio(audio_file)
                st.text_area("Transcription", value=transcription, height=300)
                st.write("done")
                pro = JOURNAL_PROMPT + transcription
                res = llm.invoke(pro)
                # st.write(pro)
                st.write(res.content)
                

