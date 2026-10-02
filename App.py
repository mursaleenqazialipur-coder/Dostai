
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


# VOICE TO TEXT
audio = st.audio_input(
    "🎙️ Bolo — Dost AI tumhari awaaz ko text mein badlega"
)

if audio:
    try:
        audio_bytes = audio.getvalue()

        with st.spinner("🎙️ Awaaz ko text mein badal raha hoon..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(
                        data=audio_bytes,
                        mime_type=audio.type
                    ),
                    "Is audio mein jo kaha gaya hai, usay bilkul waise hi text mein likho. Urdu, Roman Urdu ya English mein jo zaban ho, wahi rakho."
                ]
            )

        text = (response.text or "").strip()

        if text:
            st.session_state.messages.append(
                {"role": "user", "content": text}
            )
            st.rerun()
        else:
            st.warning("Awaaz samajh nahi aayi. Dobara boliye.")

    except Exception as e:
        st.error(f"Voice error: {e}")


# NORMAL CHAT
user_input = st.chat_input("Dost se baat karo...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Dost soch raha hai..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_input
                )

                answer = response.text or "Dobara koshish karein."
                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"AI error: {e}")
                
