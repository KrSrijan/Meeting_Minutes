import os
import tempfile
import logging
from moviepy.editor import VideoFileClip

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_audio_from_video(uploaded_file, mp3_file):
    try:
        duration_minutes = 20

        # Create a temporary file to save the uploaded video
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
            temp_video_file.write(uploaded_file.read())
            logging.info(f"Temporary video file created: {temp_video_file.name}")
            temp_video_path = temp_video_file.name

        # Load the video clip using the temporary file path
        logging.info(f"Loading video file: {temp_video_path}")
        video_clip = VideoFileClip(temp_video_path)

        # Set the duration for extraction in seconds
        duration = duration_minutes * 60
        logging.info(f"Video duration: {video_clip.duration} seconds")
        logging.info(f"Extracting audio for the first {duration} seconds...")

        # Ensure the duration does not exceed the video length
        if duration < video_clip.duration:
            logging.warning(f"Duration specified ({duration_minutes} minutes) exceeds video length. Upload video of less than 20 minutes.")
            raise ValueError("Video duration exceeds the allowed limit.")
            return None

        # Extract the audio from the video clip
        logging.info(f"Extracting audio for the first {duration_minutes} minutes...")
        audio_clip = video_clip.audio

        # Write the audio to the audio_buffer
        # Create a temporary file to save the extracted audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            temp_audio_path = temp_audio_file.name

            # Write the audio to the temporary audio file
            audio_clip.write_audiofile(temp_audio_path)

            # Read the audio data from the temporary audio file into the BytesIO object
            with open(temp_audio_path, 'rb') as f:
                mp3_file.write(f.read())

        return mp3_file
      # Return the audio buffer
    except Exception as e:
        logging.error(f"An error occurred during audio extraction: {e}")
        return None

    finally:
        # Close the video and audio clips
        try:
            audio_clip.close()
            video_clip.close()
        except:
            pass

        # Remove the temporary video file
        os.remove(temp_video_path)