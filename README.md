# Meeting Minutes

Welcome to the **Meeting Minutes**, a GenAI-powered application designed to transcribe video/audio recordings of meetings and automatically generate concise, accurate meeting minutes.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Supported Formats](#supported-formats)
- [Tech Stack](#tech-stack)
- [Future Improvements](#future-improvements)
- [Snapshots](#snapshots)
- [Steps to generate HF_API Token](#steps-to-create-a-huggingface-api)

## Overview

This project introduces the "Meeting Minutes", an AI-powered system designed to automate the generation of meeting minutes. By leveraging advanced speech recognition and natural language processing technologies, the app transcribes meeting recordings and produces concise, informative summaries, streamlining meeting documentation and enhancing productivity.

## Features

- **Automated Transcription**: Accurately converts speech to text using OpenAI's Whisper.
- **Abstractive Summarization**: Generates concise and informative summaries with Meta's LLaMA 3.2.
- **User-Friendly Interface**: Built with Streamlit for easy interaction and retrieval of summaries.

## Installation

1. **Clone this repository**:
   ```bash
   git clone <repo-url>
   cd meeting_minutes

2. pip install -r requirements.txt

3.  streamlit run app.py

## Usage

0. (First time users only) Update the secrets.toml file with your own HuggingFace API under the .streamlits folder, 
   If you don't have one already, see [here](#steps-to-create-a-huggingface-api) (Don't worry for the costs, it's free and open source).
1. Open the app in your browser (usually at http://localhost:8501).
2. Upload an video/audio file in a supported format (e.g., .mp4, .wav, .mp3).
3. Click Generate Minutes to transcribe and summarize the audio.
4. Review and download the generated meeting minutes in text format.

## Supported Formats

1. Video files: .mp4
2. Audio files: .wav, .mp3
3. Text files: .txt
3. Summarized output: Plain text, Markdown

## Tech Stack

Frontend: Streamlit
Backend: Python, GenAI for summarization - HuggingFace API
Transcription: Speech-to-text service integration (like Google Speech-to-Text, Whisper API)

## Future Improvements

1. Add multilingual support for transcription and summarization.
2. Customize summaries based on meeting context (e.g., brainstorming, project updates).

## Snapshots

![image](https://github.com/user-attachments/assets/dd996690-7f5d-4397-a891-d47ca06e35de)
Streamlit app interface

![minute minute pic](https://github.com/user-attachments/assets/7e784c4a-27a1-44cb-ba3e-3c141534b77c)
Generated meeting minutes



## Steps to create a HuggingFace API

1. Create an account [here](https://huggingface.co/), if you don't have already
2. If you want to use the default GenAI model (Llama 3.2 3B Insturct, this works actually great!), but since its a gated model, so you need to ask for   its permission first from its owner, that is Meta. Apply [here](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct). It gets approved in   about a week, although mine took less than 12 hours :).
3. If you are not going by the default model, just change the model_name in the secerts.toml file.
4. Now, go to the settings of your profile, after that go to tokens, and create a new one.
5. Follow on screen instructions, and you have your token now, just copy and paste it in the "api" section in the secrets.toml
 
 Note : In huggingFace, not every model is literally free to use. I couldn't get any official sources, but during my personal research on which models can be used for free with the serverless api token, the MODEL SIZE of the LLM should be less than 10GB, and in one month, only 10000 calls are allowed in the free tier. After that, one needs to pay. But ofcourse, since most of the models are open source, models can easily downloaded and used, but it takes up huge resources from the PC, so if your PC can withstand the power required, one can go for it, but it would require some small changes in the codes! 
 I will update the steps to use the LLM offline without using the API token.
