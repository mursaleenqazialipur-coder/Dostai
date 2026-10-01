import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Dost AI",
    page_icon="🤖"
)

st.title("🤖 Dost AI")
st.write("Tumhara friendly AI dost — Urdu, Roman Urdu ya English mein baat karo.")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY configure nahi hai.")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

audio = st.audio_input("🎙️ Bolo — Dost AI tumhari awaaz ko text mein badlega")

user_input = st.chat_input("Dost se baat karo...")

if audio:
            with st.spinner("🎙️ Awaaz ko text mein badal raha hoon..."):
        audio_bytes = audio.getvalue()
if audio:
    audio_bytes = audio.getvalue()

    with st.spinner("🎙️ Awaaz ko text mein badal raha hoon..."):
        try:
            result = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    "Is audio ko text mein convert karo. Jo zaban boli gayi hai usi zaban mein likho.",
                    types.Part.from_bytes(
                        data=audio_bytes,
                        mime_type=audio.type
                    )
                ]
            )

            text = result.text.strip()

            if text:
                st.session_state.messages.append(
                    {"role": "user", "content": text}
                )
                st.rerun()

        except Exception as e:
            st.error(f"Voice error: {e}")
