import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings with a dark theme
st.set_page_config(
    page_title="Streamly Streamlit Assistant",
    page_icon=":robot_face:",  # Favicon emoji
    layout="centered",  # Page layout option
    initial_sidebar_state="expanded",  # Expand the sidebar by default
)

# Custom CSS for the page to match the design
st.markdown("""
    <style>
    /* Overall page styling */
    body {
        background-color: #121212;
        color: #FFFFFF;
    }
    
    /* Chatbot title styling */
    .stTitle {
        font-size: 2.5em;
        color: #FFFFFF;
        text-align: center;
        margin-top: 20px;
    }

    /* Developer name styling */
    .developer-name {
        font-size: 1em;
        color: #888888;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Chat message styling */
    .stMarkdown p {
        color: #FFFFFF;
        background-color: #1E1E1E;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        max-width: 70%;
    }
    .stMarkdown p.user-message {
        background-color: #202020;
        margin-left: auto;
        text-align: left;
    }
    .stMarkdown p.assistant-message {
        background-color: #1E1E1E;
        margin-right: auto;
        text-align: right;
    }

    /* User chat input styling */
    .stTextInput input {
        background-color: #2D2D2D;
        color: #FFFFFF;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #181818 !important;
    }
    
    /* Select box in sidebar */
    .stSelectbox label {
        color: #FFFFFF !important;
    }
    .stSelectbox .st-bq {
        background-color: #202020;
        color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

# Google Gemini-Pro AI configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title and developer name on the page
st.title("Streamly Streamlit Assistant")

# Display the chat history
for message in st.session_state.chat_session.history:
    role = translate_role_for_streamlit(message.role)
    if role == "user":
        st.chat_message("user").markdown(message.parts[0].text)
    else:
        st.chat_message("assistant").markdown(message.parts[0].text)

# Input field for the user's message
user_prompt = st.chat_input("Enter your prompt here..!")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    st.chat_message("assistant").markdown(gemini_response.text)
