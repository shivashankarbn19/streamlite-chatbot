import os
import streamlit as st
st.title("DEMO CHATBOT")
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Set your Google API key securely (in actual deployment, use environment variables or secrets manager)
if "GOOGLE_API_KEY" in st.secrets:
    os.environ['GOOGLE_API_KEY'] = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("Please add your GOOGLE_API_KEY to Streamlit Secrets.")
    st.stop()

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")

# Set page config
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")

st.title("🤖 Gemini Chatbot")

# Initialize chat history in Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [SystemMessage(content="You are a helpful assistant.")]

# Function to interact with the LLM
def get_ai_response(user_input):
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    response = llm.invoke(st.session_state.chat_history)
    st.session_state.chat_history.append(AIMessage(content=response.content))
    return response.content

# Display chat messages
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        st.markdown(f"**You:** {message.content}")
    elif isinstance(message, AIMessage):
        st.markdown(f"**AI:** {message.content}")

# Input from the user
with st.form("chat_input_form", clear_on_submit=True):
    user_input = st.text_input("Your message:")
    submitted = st.form_submit_button("Send")

    if submitted and user_input.strip():
        ai_response = get_ai_response(user_input)
        st.experimental_rerun()
