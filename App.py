import os
import streamlit as st
from google import genai

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


# 🎙️ VOICE TO TEXT
audio = st.audio_input(
    "🎙️ Bolo — Dost AI tumhari awaaz ko text mein badlega"
)

if audio:
    audio_bytes = audio.getvalue()

    with st.spinner("🎙️ Awaaz ko text mein badal raha hoon..."):
        try:
            audio_file = client.files.upload(
                file=audio_bytes,
                config={"mime_type": audio.type}
            )

            interaction = client.interactions.create(
                model="gemini-3.5-transcribe",
                input=[
                    {
                        "type": "audio",
                        "uri": audio_file.uri,
                        "mime_type": audio_file.mime_type,
                    }
                ]
            )

            text = interaction.output_text.strip()

            if text:
                st.session_state.messages.append(
                    {"role": "user", "content": text}
                )
                st.rerun()

        except Exception as e:
            st.error(f"Voice error: {e}")


# 💬 NORMAL CHAT
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
                    model="gemini-3.5-flash-lite",
                    contents=user_input
                )

                answer = response.text
                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"AI error: {e}")
