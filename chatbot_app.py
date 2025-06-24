# chatbot_app.py

import streamlit as st
import wikipedia
import wolframalpha
from gtts import gTTS
import speech_recognition as sr
import tempfile
import os

# === TTS Function using gTTS ===
def SpeakText(command):
    try:
        tts = gTTS(text=command, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name)
    except Exception as e:
        st.warning("Audio playback failed.")

# === Search Function ===
def search(query, app_id):
    try:
        client = wolframalpha.Client(app_id)
        res = client.query(query)
        answer = next(res.results).text
        st.success(f"WolframAlpha Answer: {answer}")
        SpeakText("Your answer is " + answer)
    except Exception as e:
        try:
            summary = wikipedia.summary(query, sentences=2)
            st.info(f"Wikipedia Summary:\n{summary}")
            SpeakText("According to Wikipedia, " + summary)
        except Exception as we:
            st.error("No results found in WolframAlpha or Wikipedia.")
            SpeakText("Sorry, I couldn't find anything.")

# === Voice Input Function ===
def listen_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙 Listening... Speak now.")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        try:
            speech_text = r.recognize_google(audio)
            st.success(f"Recognized Speech: {speech_text}")
            return speech_text
        except sr.UnknownValueError:
            st.warning("Could not understand audio.")
        except sr.RequestError as e:
            st.error(f"Speech service error: {e}")
    return ""

# === Streamlit UI ===
st.title("🤖 Voice/Text Intelligent Search Assistant")
st.markdown("*Developed by:* Muhammed Hunais C P | Data Science @iPECsolutions.com")

st.markdown("Enter your query below or use your voice:")

# WolframAlpha App ID input
app_id = st.text_input("🔑 Enter your WolframAlpha App ID:", type="password")

# Voice input
use_voice = st.checkbox("🎤 Use voice instead of text", value=False)

query = ""

if use_voice:
    if st.button("🎙 Start Listening"):
        query = listen_voice()
else:
    query = st.text_input("✍ Type your question:")

if st.button("🔍 Search"):
    if not app_id:
        st.warning("Please enter your WolframAlpha App ID.")
    elif query.strip() == "":
        st.warning("Please provide a query.")
    else:
        search(query.lower(), app_id)
