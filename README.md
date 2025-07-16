🎥 YouTube Video Summarizer with Cohere API
A web-based application that automatically converts YouTube video transcripts into structured, easy-to-read notes using Cohere’s Large Language Models (LLMs).

Ideal for students, content creators, or professionals looking to quickly digest long videos into concise summaries.


✅ Key Features
Transcript Extraction: Automatically fetches transcripts from YouTube videos (if available).

AI-Powered Summarization: Utilizes Cohere's command model to summarize video content into bullet points.

Chunking for Large Transcripts: Handles long transcripts by splitting them into smaller pieces before summarization.

Streamlit Web UI: Simple, responsive interface built with Streamlit for easy interaction.

API Key Flexibility: Supports both .env-based secret management and optional hardcoded API key fallback for local testing.

🛠️ Technology Stack
Component	Description
Language	Python 3.8+
Frontend	Streamlit
Backend	Cohere API (command model)
Transcript	YouTube Transcript API
Environment	Python-Dotenv


📌 Usage Notes
Transcript Availability:
Some YouTube videos may not have public transcripts (e.g., music videos or private content).

Cohere Quotas & Limits:
Make sure your Cohere API key has sufficient quota for the command model usage.

Deployment:
For deploying this on platforms like Streamlit Cloud, configure environment variables in the service’s secrets manager rather than relying on .env files.

🔐 Environment Variables
Variable	Required	Description
CO_API_KEY	Yes	Your personal Cohere API key

📁 Project Folder Structure


youtube-video-summarizer/
├── app.py                # Main Streamlit application
├── .env.example          # Template for API key configuration
├── requirements.txt      # Python package dependencies
├── .gitignore            # Files and folders to ignore in Git
