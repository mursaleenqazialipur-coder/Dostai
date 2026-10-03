import os
import hashlib
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

# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = ""

# AI RESPONSE WITH FALLBACK
def ask_ai(contents):
    models = ["gemini-3.8-flash", "gemini-3.7-flash"]

    last_error = None

    for model in models:
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents
            )
            return response.text or "Dobara koshish karein."

        except Exception as e:
            last_error = e

    raise last_error


# SHOW CHAT HISTORY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# VOICE INPUT
audio = st.audio_input(
    "🎙️ Bolo — Dost AI tumhari awaaz ko text mein badlega"
)

if audio:
    audio_bytes = audio.getvalue()
    audio_hash = hashlib.sha256(audio_bytes).hexdigest()

    if audio_hash != st.session_state.last_audio_hash:

        st.session_state.last_audio_hash = audio_hash

        try:
            with st.spinner("🎙️ Awaaz samajh raha hoon..."):

                voice_text = ask_ai([
                    types.Part.from_bytes(
                        data=audio_bytes,
                        mime_type=audio.type
                    ),
                    "Is audio mein jo kaha gaya hai, usay bilkul waise hi text mein likho. Urdu, Roman Urdu ya English mein jo zaban ho, wahi rakho. Sirf bole gaye alfaaz likho."
                ])

                voice_text = voice_text.strip()

            if voice_text:
                st.session_state.messages.append({
                    "role": "user",
                    "content": voice_text
                })

                with st.spinner("Dost jawab de raha hai..."):
                    answer = ask_ai(voice_text)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                st.rerun()

            else:
                st.warning("Awaaz samajh nahi aayi. Dobara boliye.")

        except Exception as e:
            st.error(
                "Voice error: Server busy hai ya connection mein masla hai. "
                "Thori dair baad dobara try karein."
            )
            st.caption(str(e))


# NORMAL TEXT CHAT
user_input = st.chat_input("Dost se baat karo...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Dost soch raha hai..."):
            try:
                answer = ask_ai(user_input)

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error("AI server busy hai. Thori dair baad try karein.")
                st.caption(str(e))
