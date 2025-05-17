import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Set page title and icon
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("🤖 Gemini Chatbot")

# Load API key from Streamlit secrets
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("GOOGLE_API_KEY not found in Streamlit secrets.")
    st.stop()

# Initialize the Gemini LLM through LangChain
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Session state: chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [SystemMessage(content="You are a helpful assistant.")]

# Display past conversation
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").markdown(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("ai").markdown(msg.content)

# Chat input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user input
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    # Exit on "quit"
    if user_input.lower().strip() == "quit":
        st.write("👋 Chat ended.")
        st.stop()

    # Generate and show AI response
    try:
        result = llm.invoke(st.session_state.chat_history)
        ai_response = result.content
    except Exception as e:
        ai_response = f"❌ Error: {e}"

    st.chat_message("ai").markdown(ai_response)
    st.session_state.chat_history.append(AIMessage(content=ai_response))
