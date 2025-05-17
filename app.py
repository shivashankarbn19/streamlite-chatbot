import streamlit as st
import google.generativeai as genai
st.title("DEMO CHATBOT")
# Load API key from Streamlit secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Please set your GOOGLE_API_KEY in Streamlit secrets.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# Create a Gemini chat model instance
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize or get chat history
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.set_page_config(page_title="Gemini Chatbot")
st.title("🤖 Gemini Chatbot")

# Display message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# Input field
user_input = st.chat_input("Ask something...")

if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "text": user_input})

    # Get response from Gemini
    try:
        response = st.session_state.chat.send_message(user_input)
        response_text = response.text
    except Exception as e:
        response_text = f"Error: {e}"

    # Display response
    st.chat_message("ai").markdown(response_text)
    st.session_state.messages.append({"role": "ai", "text": response_text})
