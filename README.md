# Interview Practice Partner - AI Conversational Agent

An AI-powered interview practice agent that conducts mock interviews for various roles,
provides contextual follow-up questions, and delivers detailed post-interview feedback.

## Features

- Interactive conversational AI agent powered by Google Gemini 2.0 Flash
- Supports custom roles (software engineer, data scientist, etc.) and experience levels
- Maintains conversation context to ask relevant follow-up questions
- Generates detailed post-interview feedback analyzing communication and technical skills
- Simple web UI for text-based interaction

## Architecture

- **Backend:** FastAPI Python server managing conversation sessions and agent logic
- **LLM:** Google Gemini 2.0 Flash model accessed via Google’s Generative AI SDK
- **Frontend:** React + Material UI providing user-friendly chat interface
- **Session Management:** In-memory storage of agent state, Q&A, and feedback

## Setup Instructions

### Prerequisites

- Python 3.12+
- Node.js 16+
- Gemini API key from Google AI Studio

### Backend Setup

cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Create .env file with Gemini API key
echo "GEMINI_API_KEY=your_api_key" > .env

Run backend server
python main.py

### Frontend Setup

cd frontend
npm install
npm start

Access frontend UI at `http://localhost:3000`

## Usage

1. Select interview role and experience level
2. Start interview and answer questions conversationally
3. Receive detailed feedback at the end
4. Restart interview as needed

## Design Decisions

- Use of Gemini LLM for advanced contextual understanding and question generation  
- Separation of backend API and React frontend for scalability and maintainability  
- Clear session state management enabling multi-turn conversations  
- Focus on conversational quality and adaptive questioning  

## Demo Video Overview

- Role and experience selection  
- Live interview session with multiple question-answer turns  
- Ending interview and viewing AI-generated personalized feedback  
- Handling varied user personas and inputs  

## Future Enhancements

- Voice input/output integration for natural spoken interaction  
- Industry-specific question banks and adaptive difficulty scaling  
- Multi-language support and accessibility improvements  
- Persistent session storage and user profiles 
