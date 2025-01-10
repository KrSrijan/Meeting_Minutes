import logging
from huggingface_hub import InferenceClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_inference_client(api_token):
    """Set up the Hugging Face Inference Client."""
    # Set up the Inference Client with API key
    inference_client = InferenceClient(api_key=api_token)
    return inference_client

def generate_meeting_minutes(transcription, inference_client, model_name):
    """Generate meeting minutes from transcription using Hugging Face's chat completions API."""

    logging.info(f"***********************|||||********Model Name: {model_name}****************")

    system_message = (
        "You are an assistant that produces minutes of meetings from transcripts, "
        "with summary, key discussion points, takeaways, and action items with owners, in markdown."
    )

    user_prompt = f"Below is an extract transcript of a meeting. Please write minutes in markdown, including a summary with attendees, location, and date; discussion points; takeaways; and action items with owners. If it doesn't look like a meeting, just generate a good summary of the transcript. Transcript:\n{transcription}"

    # Create the list of messages for chat-based interaction
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt}
    ]

    try:
        # Make the request to the Hugging Face API using the chat completion method
        stream = inference_client.chat.completions.create(
            model=model_name,  # Pass the model name dynamically
            messages=messages,
            max_tokens=2000,  # Limit the response size if necessary
            stream=True  # Set to True for streamed responses
        )

        # Collect the streamed response and generate the meeting minutes
        generated_text = ""
        for chunk in stream:
            generated_text += chunk["choices"][0]["delta"]["content"]
        
        return generated_text

    except Exception as e:
        logging.error(f"Error during generation: {e}")
        raise

def meeting_minutes_llm(transcription, model_name, api_token):
    """Main function to generate minutes from transcription."""
    logging.info("Starting the meeting minutes generation process.")

    # Set up the inference client
    inference_client = setup_inference_client(api_token)

    # Generate minutes
    minutes_generator = generate_meeting_minutes(transcription, inference_client, model_name)

    # Accumulate the streamed output
    full_minutes = ""
    for minutes_chunk in minutes_generator:
        full_minutes += minutes_chunk  # Accumulate the chunks

    yield full_minutes  # Yield the complete minutes only once