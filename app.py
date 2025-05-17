import streamlit as st
import google.generativeai as genai

# Load API key from Streamlit secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Please set your GOOGLE_API_KEY in Streamlit secrets.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=api_key)

# Create a Gemini model instance (you can also use "gemini-1.5-pro" if preferred)
model = genai.GenerativeModel("gemini-1.5-flash")

# Set up Streamlit page
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("🤖 Gemini Chatbot")

# Initialize chat session
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# User input box
user_input = st.chat_input("Say something...")

# When user sends a message
if user_input:
    # Show user message in chat
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "text": user_input})

    try:
        # Send to Gemini API and get response
        response = st.session_state.chat.send_message(user_input)
        response_text = response.text
    except Exception as e:
        response_text = f"❌ Error: {e}"

    # Show AI response
    st.chat_message("ai").markdown(response_text)
    st.session_state.messages.append({"role": "ai", "text": response_text})
