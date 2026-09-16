import os
import streamlit as st
from google import genai
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Dost AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .header-title {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .category-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background-color: #E8F4F8;
        color: #2E86AB;
        border-radius: 1rem;
        font-size: 0.85rem;
        margin: 0.25rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<p class="header-title">🤖 Dost AI</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Tumhara Friendly AI Assistant — Urdu, Roman Urdu ya English mein baat karo</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings & Help")
    
    st.subheader("📚 Dost AI Se Kya Pooch Sakte Ho?")
    
    capabilities = {
        "💼 Business": [
            "Business ideas aur planning",
            "Marketing strategies",
            "Financial advice",
            "Job interview tips"
        ],
        "📚 Education": [
            "Concepts explain karna",
            "Assignment help",
            "Study tips",
            "Research guidance"
        ],
        "✍️ Writing": [
            "Essays likhai",
            "Creative stories",
            "Professional emails",
            "Content ideas"
        ],
        "💻 Coding": [
            "Code explain karna",
            "Bugs fix karna",
            "Programming tutorials",
            "Technology concepts"
        ],
        "💡 Ideas": [
            "Project ideas",
            "Brainstorming",
            "Problem solving",
            "Innovation tips"
        ],
        "📋 Daily Tasks": [
            "To-do lists banana",
            "Time management",
            "Health tips",
            "Daily routines"
        ]
    }
    
    selected_category = st.selectbox(
        "🎯 Category select karo:",
        list(capabilities.keys())
    )
    
    st.write("**Is category mein ask kar sakte ho:**")
    for item in capabilities[selected_category]:
        st.write(f"• {item}")
    
    st.divider()
    
    st.subheader("🌐 Language Options")
    st.info("Urdu 🇵🇰, Roman Urdu, ya English 🇬🇧 - jo bhi comfortable ho!")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.success("Chat history clear ho gai!")
    
    st.divider()
    
    st.subheader("ℹ️ About")
    st.write("""
    **Dost AI** aik friendly AI assistant hai jo:
    - Multiple languages mein baat kare
    - Business, education, coding, writing, ideas aur daily tasks mein madad de
    - Practical aur clear jawab de
    - Respectful aur helpful rahe
    """)

# API Key validation
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY abhi configure nahi hai.")
    st.info("Please set GEMINI_API_KEY environment variable")
    st.stop()

# Initialize Gemini client
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"❌ API connection error: {str(e)}")
    st.stop()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "model" not in st.session_state:
    st.session_state.model = "gemini-2.0-flash"

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# System prompt for general-purpose assistant
SYSTEM_PROMPT = """Tum Dost AI ho, ek friendly aur helpful AI assistant. Tum ek general-purpose AI assistant ho jo har tarah ke sawaloon ka jawab de sakta hai.

**Tum in sabse madad kar sakte ho:**

1. **💼 Business**: Business ideas, strategies, planning, marketing, finances, career advice
2. **📚 Education**: Concepts explain karna, assignment help, study tips, research guidance
3. **✍️ Writing**: Essays, creative writing, professional emails, content creation
4. **💻 Coding**: Code explanation, debugging, tutorials, programming concepts
5. **💡 Ideas**: Project ideas, brainstorming, problem-solving, innovation
6. **📋 Daily Tasks**: Productivity, time management, health tips, lifestyle advice
7. **🌍 General Knowledge**: News, history, science, culture, entertainment
8. **🔧 Technical Help**: Troubleshooting, how-to guides, tool recommendations

**Tum yeh follow karo:**
- User Urdu, Roman Urdu ya English mein baat kar sakta hai - uski language mein jawab do
- Jawab clear, practical aur easy-to-understand ho
- Detailed examples aur step-by-step guidance de
- Agar kisi topic ko detail se samjhana ho to structured format use kar
- Respectful, helpful, aur friendly attitude rakho
- Har sawal ko seriously lo, khahye woh chota ya bada
- Agar tum kuch nahi jante to honestly kaho aur assistance offer karo

User kya pooch raha hai uske mutabiq context-aware jawab do. Agar coding question ho to code snippets do. Agar writing help ho to suggestions de. Agar business ho to practical advice de.

Tum ek trusted dost ho - helpful, knowledgeable, aur always supportive."""

# Chat input
user_input = st.chat_input("Dost AI se kuch bhi pooch sakta hai... 😊", key="chat_input")

if user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Dost soch raha hai... 🤔"):
            try:
                # Prepare message history for API
                message_history = []
                for msg in st.session_state.messages[:-1]:  # Exclude the current user message
                    message_history.append({
                        "role": msg["role"],
                        "parts": [{"text": msg["content"]}]
                    })
                
                # Add current user message
                message_history.append({
                    "role": "user",
                    "parts": [{"text": user_input}]
                })
                
                # Call Gemini API
                response = client.models.generate_content(
                    model=st.session_state.model,
                    contents=message_history,
                    config={
                        "system_instruction": SYSTEM_PROMPT,
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "top_k": 40,
                        "max_output_tokens": 2048,
                    }
                )
                
                assistant_message = response.text
                
                # Add assistant message to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
                # Display response
                st.markdown(assistant_message)
                
            except Exception as e:
                error_message = f"❌ Error: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🇵🇰 Made with ❤️ for Urdu speakers")
with col2:
    st.caption(f"⏰ {datetime.now().strftime('%d %B %Y')}")
with col3:
    st.caption("Powered by Google Gemini")
