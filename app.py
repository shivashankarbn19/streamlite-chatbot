import streamlit as st
import google.generativeai as genai

# Load API key from Streamlit secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Please set your GOOGLE_API_KEY in Streamlit secrets.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=api_key)

# Create a Gemini model instance
model = genai.GenerativeModel("gemini-1.5-flash")

# Set up Streamlit page
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("🤖 Gemini Chatbot")

# Initialize chat session
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# Input from user
user_input = st.chat_input("Say something...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "text": user_input})

    # Get response from Gemini
    try:
        response = st.session_state.chat.send_message(user_input)
        ai_text = response.text
    except Exception as e:
        ai_text = f"❌ Error: {e}"

    # Show AI message
    st.chat_message("ai").markdown(ai_text)
    st.session_state.messages.append({"role": "ai", "text": ai_text})
