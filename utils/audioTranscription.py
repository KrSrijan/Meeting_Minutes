import logging
import faster_whisper

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transcribe_audio(audio_buffer): 
    """Transcribe audio file to text using Faster Whisper.

    Args:
        audio_buffer (audio buffer): audio file buffer to transcribe.

    Returns:
        Optional[str]: The transcription text if successful, None otherwise.
    """
    try:
        logging.info(f"Starting transcription for file: {audio_buffer}")

        # Load the Faster Whisper model
        model = faster_whisper.WhisperModel("base")  # Choose your desired model size
        # model = faster_whisper.WhisperModel("large-v2") # A bigger model for better performance

        # Transcribe the audio
        segments, info = model.transcribe(audio_buffer, beam_size=5) 

        # Extract the transcribed text from segments
        transcription = ''.join([segment.text for segment in segments])

        logging.info("Transcription complete.")

        return transcription

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

    return None

def audio_transcription(audio_buffer):  # Remove openai_api_key argument
    """Main function to handle transcription."""

    transcription = transcribe_audio(audio_buffer)

    if transcription:
        logging.info(f"Transcription Result: {transcription}")
    else:
        logging.info("Transcription failed.")

    return transcription