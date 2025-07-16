import streamlit as st
from dotenv import load_dotenv
import os
import time
import urllib.parse
import cohere
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    VideoUnavailable,
    TranscriptsDisabled,
    NoTranscriptFound,
)

# Load environment variables
load_dotenv()
cohere_api_key = os.getenv("CO_API_KEY") or "8TF84n4VRjxYkV3oTBZ1bTy1x2qtgcR924RjMkp6"

if not cohere_api_key or cohere_api_key == "your_actual_cohere_api_key_here":
    st.warning("⚠️ Using hardcoded Cohere API key. For safety, use a .env file in production!")
cohere_client = cohere.Client(cohere_api_key)

prompt_template = """You are a YouTube video summarizer. You will take the transcript text
and summarize the entire video, providing the important summary in bullet points
within 250 words. Please provide the summary of the text given here:\n\n"""

def extract_video_id(url):
    parsed_url = urllib.parse.urlparse(url)
    if "youtube.com" in parsed_url.netloc:
        query = urllib.parse.parse_qs(parsed_url.query)
        return query.get("v", [None])[0]
    elif "youtu.be" in parsed_url.netloc:
        return parsed_url.path.strip("/")
    return None

def extract_transcript_details(youtube_video_url):
    try:
        video_id = extract_video_id(youtube_video_url)
        if not video_id:
            st.error("❌ Invalid YouTube URL format.")
            return None

        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([entry["text"] for entry in transcript_data])
        return transcript

    except VideoUnavailable:
        st.error("❌ The video is unavailable or restricted.")
    except TranscriptsDisabled:
        st.error("❌ Transcripts are disabled for this video.")
    except NoTranscriptFound:
        st.error("❌ No transcript found for this video.")
    except Exception as e:
        st.error(f"⚠️ Unexpected error: {e}")
    return None

def chunk_text(text, max_chars=2000):
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

def generate_cohere_content(text_chunk, prompt):
    try:
        response = cohere_client.generate(
            model='command-r-plus',
            prompt=prompt + text_chunk,
            max_tokens=1000,
            temperature=0.3,
            stop_sequences=["--END--"]
        )
        return response.generations[0].text.strip()
    except Exception as e:
        st.warning(f"⚠️ Cohere API error: {e}")
        return "Error occurred while generating content."

st.set_page_config(page_title="YouTube Summarizer", layout="centered")
st.title("🎥 YouTube Videos to Detailed Notes Converter")

youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = extract_video_id(youtube_link)
    if video_id:
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button("📝 Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        st.info("⏳ Generating summary using Cohere...")
        chunks = chunk_text(transcript_text)

        summaries = []
        for idx, chunk in enumerate(chunks):
            st.write(f"🔹 Processing chunk {idx + 1} of {len(chunks)}...")
            summary = generate_cohere_content(chunk, prompt_template)
            summaries.append(summary)

        final_summary = "\n\n".join(summaries)
        st.markdown("## 🧾 Detailed Notes:")
        st.write(final_summary)
