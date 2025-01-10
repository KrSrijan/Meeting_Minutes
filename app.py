import os
import io
import logging
import streamlit as st
from utils.extractAudio import extract_audio_from_video
from utils.audioTranscription import audio_transcription
from utils.lamaModelHandlerCPU import meeting_minutes_llm

# Vars
LLAMA = st.secrets["LLAMA"]['model_name']  # Access the model_name directly
HF_TOKEN = st.secrets["HF_TOKEN"]["api_token"]  # Access the api_token directly

# Configure logging
logging.basicConfig(level=logging.INFO)


def process_file_transcription(uploaded_file):  # Removed api_key argument
    """Process the uploaded file to generate transcription of the meeting"""

    file_extension = os.path.splitext(uploaded_file.name)[-1].lower()
    audio_file = None

    # Create an in-memory file-like object for the audio extraction
    audio_buffer = io.BytesIO()

    # Determine file type and process accordingly
    try:
        if file_extension in [".mp4", ".mov"]:  # Check if the uploaded file is a video
            # Extract audio and write to an in-memory buffer
            extract_audio_from_video(uploaded_file, audio_buffer)  # No need to assign to audio_buffer
            logging.info("Extracted audio from video.")
            audio_buffer.seek(0)  # Move the cursor to the beginning of the buffer

        elif file_extension in [".wav", ".mp3", ".m4a"]:  # Check if the uploaded file is audio
            audio_buffer = uploaded_file
            logging.info("Using uploaded audio file directly.")

        elif file_extension in [".txt"]:  # Check if the uploaded file is audio
            logging.info("Using text file directly.")
            transcription = uploaded_file.read().decode("utf-8")
            return transcription
        else:
            st.error("Unsupported file type. Please upload an audio or video file.")
            return None

        # Transcribe the audio to text
        transcription = audio_transcription(audio_buffer)  # No need to pass api_key
        logging.info("Transcription completed.")

        return transcription

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        st.error("An error occurred while processing the file. Please try again.")
        return None


# App Title and Logo
st.set_page_config(page_title="Meeting Minutes LLM", page_icon="📝", layout="wide")
st.title("📋 Meeting Minute")
st.write("Skip the note-taking and enjoy the conversation—just upload your meeting audio or video, and let us handle the minutes effortlessly!")

# Sidebar for LLM Selection (removed API Key Input)
with st.sidebar:
    st.header("⚙️ Settings")
    st.write("Configure your LLM settings here.")

    # Choice of LLMs
    llm_choice = st.selectbox(
        "🤖 Choose your LLM",
        [
            "meta-llama/Llama-3.2-3B-Instruct (Fast, good for general use)",
            "meta-llama/Llama-2-13b-chat-hf (More powerful, may be slower) *requires pro subscription*",
            "Custom Model"
        ],
        help="Select the language model you want to use."
    )

    if llm_choice == "Custom Model":
        custom_model_name = st.text_input("Enter custom model name:", value="", help="Enter the full Hugging Face model name (e.g., google/flan-t5-xl)")
        # API Key Input
        api_key = st.text_input("🔑 API Key", type="password", help="Enter your LLM API Key")
    else:
        custom_model_name = None  # No custom model selected

# Main Section for Audio/Video Upload
st.subheader("📁 Upload Meeting Audio/Video")
uploaded_file = st.file_uploader("Upload an audio or video file", type=["wav", "mp3", "m4a", "mp4", "mov", "txt"])

# Check if a file has been uploaded
if uploaded_file:
    # Display the file name
    st.write("File uploaded successfully:", uploaded_file.name)

    # Display audio player if the file is an audio format
    if uploaded_file.type.startswith("audio"):
        st.audio(uploaded_file, format=uploaded_file.type)

    # Display video player if the file is a video format
    elif uploaded_file.type.startswith("video"):
        st.video(uploaded_file, format=uploaded_file.type)
    elif uploaded_file.type == "text/plain":
        st.write("Text file uploaded successfully.")

    st.write("Generating minutes... please wait 🚀")  # Removed api_key check

    transcription = process_file_transcription(uploaded_file)  # No need to pass api_key

    if transcription:  # Check if transcription was successful
        with st.spinner("Processing..."):
            # Pass custom_model_name to meeting_minutes_llm if provided
            if custom_model_name:
                meeting_minutes_generator = meeting_minutes_llm(transcription, LLAMA, HF_TOKEN, custom_model_name)
            else:
                logging.info(f"Using default model: {LLAMA}")
                meeting_minutes_generator = meeting_minutes_llm(transcription, model_name=LLAMA, api_token=HF_TOKEN)

            # Display each piece of generated text as it comes in
            # Display each piece of generated text as it comes in
        for i, minutes in enumerate(meeting_minutes_generator):  # Use enumerate to get the index
            st.text_area("📜 **Meeting Minutes Generated:**", value=minutes, height=300, key=f"minutes_{i}")  # Use f-string to create unique key
    else:
        st.error("Transcription failed. Please try again.")  # Handle transcription failure

else:
    st.info("Please upload an audio or video file to start processing.")  # Removed api_key message

# Custom CSS for modern styling
st.markdown(
    """
    <style>
    .css-1aumxhk, .css-18e3th9 {
        background: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
    }
    .st-bd {
        border: 2px solid #e1e5e9;
    }
    .stSidebar, .stButton>button {
        background: #0073e6 !important;
        color: #fff !important;
    }
    .stSelectbox {
        height: 60px;  /* Adjust the height as needed */
    }
    </style>
    """,
    unsafe_allow_html=True
)