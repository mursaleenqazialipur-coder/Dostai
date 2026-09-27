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
    st.error("GEMINI_API_KEY missing hai.")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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
                system_instruction = (
                    "Tum Dost AI ho, ek friendly aur intelligent AI companion. "
                    "User jis language mein baat kare, usi language mein jawab do. "
                    "Urdu, Roman Urdu aur English support karo. "
                    "Seedha, natural aur helpful jawab do. "
                    "User ne na poocha ho to earning ya freelancing ki advice mat do."
                )

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_input,
                    config={
                        "system_instruction": system_instruction
                    }
                )

                answer =
