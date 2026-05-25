# Quiz Generator Backend API

Built as part of a full-stack learning journey.

This project is a **RESTful backend API for generating quizzes from YouTube videos** using **Django** and **Django Rest Framework**.

The API allows users to submit a video URL, automatically process the content 
(audio → transcription → AI), 
and generate structured quizzes.

This project was created to **practice backend architecture, external service integration, and AI-driven data pipelines**.

---

# Features

* User registration and authentication (JWT via HTTP-only cookies)
* Secure login, logout, and token refresh flow
* Quiz generation from YouTube videos
* Automatic audio extraction and transcription (Whisper)
* AI-based quiz generation (LLM integration)
* Quiz CRUD (create, read, update, delete)
* Strict serializer validation (no silent field ignoring)

---

# Technologies

* Python 3.x  
* Django  
* Django Rest Framework  
* SimpleJWT (cookie-based authentication)  
* yt-dlp (audio extraction)  
* Whisper (speech-to-text)  
* Gemini / LLM API (quiz generation)  
* SQLite (default Django database)

---

# Authentication

Authentication is handled using **JWT stored in HTTP-only cookies**.

* `access_token` → short-lived authentication  
* `refresh_token` → used to generate new access tokens  

### Flow

* Login sets both cookies  
* Requests are authenticated via:
  - Authorization header **or**
  - `access_token` cookie  
* Refresh endpoint issues a new access token  
* Logout deletes both cookies  

---

# Permissions

The API uses a custom permission system:

* **Admin Access**  
  Admin users can access and manage all quizzes.

* **Quiz Ownership**  
  Users can only access and modify quizzes they created.

* **Protected Endpoints**  
  All quiz-related endpoints require authentication.

---

# Core Logic

The main pipeline is built around automated quiz generation:

### Quiz Creation Flow

1. Normalize and validate YouTube URL  
2. Download audio using `yt-dlp`  
3. Transcribe audio using Whisper  
4. Truncate transcript (token limit handling)  
5. Generate quiz via LLM  
6. Parse structured JSON response  
7. Store quiz in database  

---

### Important Constraints

* Only valid YouTube URLs are accepted  
* Transcript length is limited to avoid LLM overload  
* LLM output must be valid JSON  
* Unknown fields in update requests are rejected  

---

# Installation

Clone the repository:

```
git clone <repository-url>
cd Quizly
```

Create a virtual environment:

```
python -m venv .venv
```

Activate the environment:

Linux / Mac

```
source .venv/bin/activate
```

Windows

```
.venv\Scripts\activate
```

Install FFmpeg (required for Whisper and yt-dlp):

Linux

```
sudo apt install ffmpeg
```

Windows

```
winget install ffmpeg
```

macOS

```
brew install ffmpeg
```

Install dependencies:

```
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

You can generate a Gemini API key from Google AI Studio.

Run migrations:

```
python manage.py migrate
```

Start the development server:

```
python manage.py runserver
```

---

# Purpose of this Project

This project was built to practice:

* Django Rest Framework  
* JWT authentication with cookies  
* secure API design  
* external service integration (yt-dlp, Whisper, LLMs)  
* building AI-powered pipelines  
* validation and error handling  
* structuring scalable backend logic  

---

# License

This project is intended for **educational purposes**.