import streamlit as st
import whisper
import tempfile
model = whisper.load_model("base")
import os
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
        
        if st.button("Summarise"):
            with st.spinner("Summarising the Audio..."):
                transcription = transcribe_audio(audio_file)
                st.text_area("Transcription", value=transcription, height=300)
                

