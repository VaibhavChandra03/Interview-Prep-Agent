from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
from agents.interview_agent import InterviewAgent
from config import get_settings

router = APIRouter()

# In-memory session storage
sessions = {}

class StartInterviewRequest(BaseModel):
    role: str
    experience_level: str

class RespondRequest(BaseModel):
    session_id: str
    user_response: str
    end_interview: bool = False

@router.post("/start-interview")
async def start_interview(request: StartInterviewRequest):
    """Start a new interview session"""
    try:
        settings = get_settings()
        session_id = str(uuid.uuid4())
        
        # Create agent for this session
        agent = InterviewAgent(settings.gemini_api_key)
        
        # Setup interview and get first question
        first_question = agent.setup_interview(request.role, request.experience_level)
        
        # Store session
        sessions[session_id] = {
            "agent": agent,
            "role": request.role,
            "experience_level": request.experience_level,
            "questions_asked": [first_question],
            "user_responses": [],
            "feedback_notes": []
        }
        
        return {
            "session_id": session_id,
            "question": first_question,
            "phase": "interviewing"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/respond")
async def respond(request: RespondRequest):
    """Process user response and return next question or feedback"""
    try:
        if request.session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = sessions[request.session_id]
        agent = session["agent"]
        
        # Get current question
        current_question = session["questions_asked"][-1] if session["questions_asked"] else ""
        
        # Analyze response
        analysis = agent.analyze_response(
            current_question,
            request.user_response,
            session["role"]
        )
        session["feedback_notes"].append(analysis)
        
        # Store Q&A
        session["user_responses"].append({
            "question": current_question,
            "answer": request.user_response
        })
        
        # Check if interview should end
        if request.end_interview or len(session["questions_asked"]) >= 6:
            # Generate final feedback
            feedback = agent.generate_feedback(
                session["role"],
                session["experience_level"],
                session["user_responses"]
            )
            
            sessions[request.session_id]["final_feedback"] = feedback
            
            return {
                "text": feedback,
                "phase": "completed",
                "is_complete": True
            }
        else:
            # Ask next question
            next_question = agent.ask_question(
                session["role"],
                session["experience_level"],
                session["user_responses"]
            )
            session["questions_asked"].append(next_question)
            
            return {
                "text": next_question,
                "phase": "interviewing",
                "is_complete": False
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feedback/{session_id}")
async def get_feedback(session_id: str):
    """Get final feedback for a completed interview"""
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = sessions[session_id]
        feedback = session.get("final_feedback")
        
        if not feedback:
            raise HTTPException(status_code=400, detail="Interview not completed yet")
        
        return {
            "feedback": feedback,
            "qa_history": session["user_responses"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
