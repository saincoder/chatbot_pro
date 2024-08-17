import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import io

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
        background: linear-gradient(to right, #2c3e50, #bdc3c7);
        color: #FFFFFF;
        font-family: 'Arial', sans-serif;
    }
    
    /* Chatbot title styling */
    .stTitle {
        font-size: 2.5em;
        color: #FFFFFF;
        text-align: center;
        margin-top: 20px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    }

    /* Developer name styling */
    .developer-name {
        font-size: 1em;
        color: #888888;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }

    /* Chat message styling */
    .stMarkdown p {
        color: #FFFFFF;
        background-color: #1E1E1E;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        max-width: 70%;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
        transition: background-color 0.3s ease;
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

    /* Button styling */
    .stDownloadButton {
        background-color: #1E1E1E;
        color: #FFFFFF;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stDownloadButton:hover {
        background-color: #333333;
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

# Function to get the first three words of a text
def get_first_three_words(text):
    return ' '.join(text.split()[:3])

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Initialize lists to store excerpts
prompts_excerpts = []
responses_excerpts = []

# Display the chatbot's title and developer name on the page
st.title("NexBot Assistant")
st.text('Developed by Shahid Hussain')
# Display the chat history
for message in st.session_state.chat_session.history:
    role = translate_role_for_streamlit(message.role)
    if role == "user":
        st.chat_message("user").markdown(message.parts[0].text)
        prompts_excerpts.append(get_first_three_words(message.parts[0].text))
    else:
        st.chat_message("assistant").markdown(message.parts[0].text)
        responses_excerpts.append(get_first_three_words(message.parts[0].text))

# Input field for the user's message
user_prompt = st.chat_input("Enter your prompt here..!")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    st.chat_message("assistant").markdown(gemini_response.text)

    # Store the excerpts of the new prompt and response
    prompts_excerpts.append(get_first_three_words(user_prompt))
    responses_excerpts.append(get_first_three_words(gemini_response.text))

# Function to convert chat history to a downloadable text file
def get_chat_history():
    chat_history = ""
    for message in st.session_state.chat_session.history:
        role = translate_role_for_streamlit(message.role)
        if role == "user":
            chat_history += f"User: {message.parts[0].text}\n"
        else:
            chat_history += f"Assistant: {message.parts[0].text}\n"
    return chat_history

# Check if chat history is empty and show appropriate message or download button in the sidebar
chat_history = get_chat_history()

with st.sidebar:
    if not chat_history.strip():
        st.write("You don't have any chat yet.")
    else:
        buffer = io.BytesIO(chat_history.encode('utf-8'))  # Convert to bytes
        st.download_button(label="Download Chat History", data=buffer, file_name="chat_history.txt", mime="text/plain", key="download_button")

    # Display excerpts
    st.subheader("Recent Prompts & Responses")
    for i in range(len(prompts_excerpts)):
        st.write(f"**User:** {prompts_excerpts[i]}")
        st.write(f"**Bot:** {responses_excerpts[i]}")
