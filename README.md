# Google-meet-transcriber

A Flask-based web application that allows users to upload Google Meet recordings (or any audio/video file) and transcribes the audio into text using AssemblyAI. Transcripts are saved in TXT, PDF, and JSON formats and can be viewed or downloaded later.

# Features

Upload audio/video files via web interface

Transcribe audio using AssemblyAI Speech-to-Text API

Save transcripts in TXT, PDF, and JSON

List all previous transcripts

Download transcripts by ID

Easy to deploy locally or on a server

# Tech Stack

Backend: Python, Flask

Frontend: HTML, JavaScript

API: AssemblyAI Speech-to-Text

Data Storage: Local file system (uploads/ + transcripts/)

PDF Generation: ReportLab

Environment Management: python-dotenv

# Folder Structure
meet-transcriber/
│
├── app.py                   # Main Flask app
├── templates/
│   ├── recorder.html        # Upload page
│   └── viewer.html          # View/download transcripts
├── uploads/                 # Uploaded audio files
├── transcripts/             # TXT, PDF, JSON transcripts
├── .env                     # Environment variables (API key)
└── README.md                # Project documentation

# Setup & Installation

# Clone the repository

git clone https://github.com/Prachikhambayat/google-meet-transcriber.git
cd google-meet-transcriber


Create and activate virtual environment

python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows


Install dependencies

pip install -r requirements.txt


Set AssemblyAI API key

ASSEMBLYAI_API_KEY=your_assemblyai_key_here


Run the Flask app

python app.py


Open in browser
http://127.0.0.1:8000

# Usage

Go to the Home Page.

Upload a Google Meet recording (mp3, wav, mp4).

Wait for transcription (progress may take time for long recordings).

View transcript in browser or download as TXT / PDF.

Access previous transcripts at /transcripts endpoint.

# API Endpoints
Endpoint	Method	Description
/upload	POST	Upload audio/video file for transcription
/transcripts	GET	List all transcript metadata
/download/<tid>/<ftype>	GET	Download transcript (txt/pdf) by ID
