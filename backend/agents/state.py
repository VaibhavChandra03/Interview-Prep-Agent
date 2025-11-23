from typing import TypedDict, List, Optional
from enum import Enum

class InterviewPhase(Enum):
    SETUP = "setup"
    INTERVIEWING = "interviewing"
    FEEDBACK = "feedback"
    COMPLETED = "completed"

class InterviewState(TypedDict):
    phase: str
    role: str
    experience_level: str
    messages: List[dict]
    questions_asked: List[str]
    user_responses: List[dict]
    current_question: Optional[str]
    feedback_notes: List[str]
