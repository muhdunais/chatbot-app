# streamlit_app.py

import streamlit as st
import wikipedia
import wolframalpha
import pyttsx3
import speech_recognition as sr
import os

# === Initialize TTS Engine ===
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

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
st.markdown("Developers: Shaheel, Ashiqu, Hunais | Data Science @iPECsolutions.com")

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