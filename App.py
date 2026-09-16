import os
import streamlit as st
from google import genai
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Dost AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto"
)

# Custom CSS for better UX
st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        background-color: #f5f5f5;
    }
    
    .main {
        max-width: 900px;
        margin: 0 auto;
    }
    
    .stChatMessage {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.75rem;
        line-height: 1.6;
    }
    
    .stChatMessage.user {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
    }
    
    .stChatMessage.assistant {
        background-color: #F5F5F5;
        border-left: 4px solid #4CAF50;
    }
    
    .header-container {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        color: white;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .chat-container {
        background-color: white;
        border-radius: 0.75rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 0.75rem;
        margin: 1rem 0;
    }
    
    .category-item {
        padding: 0.75rem;
        background-color: #E3F2FD;
        border-radius: 0.5rem;
        border: 1px solid #BBDEFB;
        text-align: center;
        font-size: 0.9rem;
    }
    
    .info-box {
        background-color: #E8F5E9;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #FFF3E0;
        border-left: 4px solid #FF9800;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .error-box {
        background-color: #FFEBEE;
        border-left: 4px solid #F44336;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    @media (max-width: 768px) {
        .header-title {
            font-size: 1.8rem;
        }
        
        .main {
            padding: 0.5rem;
        }
        
        .stChatMessage {
            padding: 0.75rem;
        }
    }
    
    .footer {
        text-align: center;
        padding: 1rem;
        color: #666;
        font-size: 0.85rem;
        margin-top: 2rem;
        border-top: 1px solid #ddd;
    }
    
    .code-block {
        background-color: #f4f4f4;
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: 'Courier New', monospace;
        overflow-x: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-container">
        <div class="header-title">🤖 Dost AI</div>
        <div class="header-subtitle">Tumhara Friendly AI Assistant</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Language preference
    language = st.radio(
        "🌐 Select Language",
        ["Urdu/Roman Urdu", "English", "Mixed"],
        horizontal=False
    )
    
    st.divider()
    
    # Capability categories
    st.subheader("📚 What Can Dost AI Help With?")
    
    capabilities = {
        "💼 Business": [
            "Business planning & ideas",
            "Marketing strategies",
            "Financial calculations",
            "Career advice",
            "Startup guidance"
        ],
        "📚 Education": [
            "Explain concepts clearly",
            "Assignment & homework help",
            "Study strategies",
            "Research guidance",
            "Exam preparation"
        ],
        "✍️ Writing": [
            "Essays & articles",
            "Creative stories",
            "Professional emails",
            "Content creation",
            "Proofreading & editing"
        ],
        "💻 Coding": [
            "Code explanations",
            "Debugging & fixes",
            "Programming tutorials",
            "Algorithm help",
            "Best practices"
        ],
        "🧮 Calculations": [
            "Math & algebra",
            "Statistics",
            "Data analysis",
            "Conversions",
            "Financial math"
        ],
        "💡 Ideas": [
            "Project ideas",
            "Problem solving",
            "Brainstorming",
            "Innovation tips",
            "Creative concepts"
        ],
        "📋 Daily Tasks": [
            "Productivity tips",
            "Time management",
            "Health & wellness",
            "Life advice",
            "General Q&A"
        ]
    }
    
    # Display categories as clickable items
    for category in capabilities.keys():
        if st.checkbox(f"✓ {category}", value=True, key=f"cat_{category}"):
            with st.expander(f"See examples for {category}"):
                for item in capabilities[category]:
                    st.write(f"• {item}")
    
    st.divider()
    
    # Chat management
    st.subheader("💬 Chat Management")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.success("Chat cleared!")
            st.rerun()
    
    with col2:
        if st.button("📥 Save Chat", use_container_width=True):
            if st.session_state.messages:
                chat_json = json.dumps(st.session_state.messages, indent=2, ensure_ascii=False)
                st.download_button(
                    "Download",
                    chat_json,
                    "dostai_chat.json",
                    "application/json",
                    use_container_width=True
                )
            else:
                st.info("No chat to save yet!")
    
    st.divider()
    
    # Model selection
    st.subheader("🔧 AI Model")
    model_choice = st.selectbox(
        "Select Model",
        ["gemini-2.0-flash", "gemini-1.5-flash"],
        help="Flash models are faster, Pro models are more powerful"
    )
    
    st.divider()
    
    # About section
    st.subheader("ℹ️ About Dost AI")
    st.markdown("""
    **Dost AI** is your friendly AI companion that:
    - 🗣️ Speaks Urdu, Roman Urdu & English
    - 🎯 Answers any question clearly & naturally
    - 💡 Helps with work, studies, coding & more
    - ⚡ Works on phones, tablets & computers
    - 🔒 No signup required
    
    **Tip:** Ask follow-up questions to get more details!
    """)

# API Key validation
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY not configured")
    st.info("Please set the GEMINI_API_KEY environment variable to use Dost AI")
    st.stop()

# Initialize Gemini client
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"❌ Connection Error: {str(e)}")
    st.stop()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "model" not in st.session_state:
    st.session_state.model = "gemini-2.0-flash"

# Enhanced system prompt for general-purpose AI
SYSTEM_PROMPT = """You are Dost AI, a friendly and helpful AI assistant that speaks Urdu, Roman Urdu, and English naturally.

**Your Personality:**
- Friendly, warm, and helpful like a trusted friend
- Clear and concise in your explanations
- Practical and actionable in your advice
- Honest about limitations
- Respectful of all users

**Your Capabilities:**

1. **💼 Business**: Business ideas, market analysis, financial advice, career guidance, startup tips, negotiation strategies
2. **📚 Education**: Explain concepts clearly, help with assignments, study tips, research guidance, exam prep, complex topics
3. **✍️ Writing**: Essays, stories, emails, content, blogs, creative writing, editing, grammar help
4. **💻 Coding**: Code explanations, debugging, tutorials, algorithm help, best practices, multiple languages
5. **🧮 Calculations**: Math, algebra, calculus, statistics, data analysis, unit conversions, financial calculations
6. **💡 Ideas**: Creative ideas, problem-solving, brainstorming, innovation, project planning
7. **📋 Daily Tasks**: Productivity, time management, health tips, life advice, general knowledge questions

**Guidelines:**
- Respond in the user's language (Urdu/Roman Urdu or English)
- Provide detailed, useful answers - not generic advice
- Use examples when helpful
- Format code with proper indentation
- For calculations, show your work
- For writing, be specific and constructive
- Ask clarifying questions if needed
- Acknowledge if something is outside your scope
- Keep responses clear and well-organized

**Response Format:**
- Use clear headings and bullet points for better readability
- For code: use proper formatting
- For lists: use clear numbering or bullets
- For complex topics: break into sections
- Keep paragraphs short and scannable

Remember: You're a helpful friend providing practical, honest assistance. Be conversational but informative."""

# Main chat interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
user_input = st.chat_input(
    "Ask Dost AI anything... (Business 💼 | Education 📚 | Coding 💻 | Writing ✍️ | Ideas 💡 | Calculations 🧮 | Daily Tasks 📋)",
    key="user_input"
)

if user_input:
    # Add user message to history immediately (so it doesn't disappear)
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Display user message immediately
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    # Generate response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Dost soch raha hai... 💭"):
            try:
                # Prepare conversation history for the API
                message_history = []
                
                for msg in st.session_state.messages:
                    message_history.append({
                        "role": msg["role"],
                        "parts": [{"text": msg["content"]}]
                    })
                
                # Call Gemini API with enhanced configuration
                response = client.models.generate_content(
                    model=model_choice,
                    contents=message_history,
                    config={
                        "system_instruction": SYSTEM_PROMPT,
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "top_k": 40,
                        "max_output_tokens": 3000,
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
                
                # Success feedback
                st.success("✓ Response generated successfully")
                
            except Exception as e:
                error_msg = f"❌ **Error:** {str(e)}\n\nPlease check your API key and try again."
                st.error(error_msg)
                
                # Still add the error to history so user sees what happened
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

# Footer with helpful info
st.markdown("""
    <div class="footer">
        <p>🇵🇰 Dost AI - Tumhara Friendly AI Assistant | Made to be helpful, honest & clear</p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem;">💡 Tip: Ask follow-up questions for more details. Type naturally in Urdu, Roman Urdu or English!</p>
    </div>
""", unsafe_allow_html=True)

# Display message count at the bottom (useful for context awareness)
if st.session_state.messages:
    message_count = len(st.session_state.messages)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"📊 Messages: {message_count}")
    with col2:
        st.caption(f"🕐 Model: {model_choice}")
    with col3:
        st.caption(f"🌐 Language: {language}")
