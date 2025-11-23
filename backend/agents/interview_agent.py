import google.generativeai as genai
from typing import Optional, List
import json

class InterviewAgent:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.conversation_history = []
    
    def setup_interview(
        self,
        role: str,
        experience_level: str,
        your_name: str = "Vaibhav",
        your_title: str = "Senior Engineer",
        company_name: str = "Eightfold.ai"
    ) -> str:
        """Initialize interview and return first question with personalized greeting"""
        self.conversation_history = []
        
        system_prompt = f"""You are an experienced professional interviewer conducting a {experience_level} {role} interview.

Your responsibilities:
1. Start with a warm greeting using your name ({your_name}), title ({your_title}), and company ({company_name})
2. Ask relevant, thoughtful questions based on the role and experience level
3. Listen to responses and ask follow-up questions naturally
4. Assess the candidate's skills, experience, and cultural fit
5. Be professional but friendly
6. Adapt your questions based on their responses

Interview Role: {role}
Experience Level: {experience_level}

Start the interview now with a welcoming greeting and first question."""

        response = self.model.generate_content(system_prompt)
        self.conversation_history.append({
            "role": "assistant",
            "content": response.text
        })
        return response.text
    
    def ask_question(self, role: str, experience_level: str, previous_responses: List[dict]) -> str:
        """Generate next interview question based on previous responses"""
        
        context = f"You are conducting a {experience_level} {role} interview."
        
        if previous_responses:
            context += f"\n\nPrevious Q&A:\n"
            for resp in previous_responses[-3:]:  # Last 3 responses for context
                context += f"Q: {resp.get('question', '')}\nA: {resp.get('answer', '')}\n\n"
        
        prompt = f"""{context}

Based on the conversation so far, ask ONE relevant follow-up question that:
- Builds naturally on their previous responses
- Explores their experience and skills deeper
- Is appropriate for the {experience_level} level
- Uses behavioral or situational questioning when possible

Ask ONLY the question. Do not include any other text."""

        response = self.model.generate_content(prompt)
        return response.text
    
    def analyze_response(self, question: str, answer: str, role: str) -> str:
        """Analyze quality of candidate's response"""
        
        prompt = f"""Analyze this interview response briefly:

Question: {question}
Answer: {answer}
Role: {role}

Note (1-2 sentences):
- How well they answered
- Clarity and structure
- Technical knowledge shown (if applicable)
- Communication quality"""

        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_feedback(self, role: str, experience_level: str, qa_history: List[dict]) -> str:
        """Generate comprehensive post-interview feedback"""
        
        qa_text = json.dumps(qa_history, indent=2)
        
        prompt = f"""You conducted a {experience_level} {role} interview. Here's the Q&A:

{qa_text}

Provide detailed feedback covering:

1. **Overall Performance** (1-2 sentences summary)
2. **Strengths** (2-3 specific points with examples from their answers)
3. **Areas for Improvement** (2-3 constructive areas)
4. **Communication Skills** (clarity, confidence, structure)
5. **Technical Knowledge** (if applicable - depth and accuracy)
6. **Recommendation** (actionable advice for next steps)

Be encouraging but honest. Use specific examples from their responses."""

        response = self.model.generate_content(prompt)
        return response.text
