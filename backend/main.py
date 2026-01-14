from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import PyPDF2
import docx
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import json

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Resume Analyzer API")

# Enable CORS (so frontend can talk to backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq AI client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ==================== HELPER FUNCTIONS ====================

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file"""
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file"""
    doc = docx.Document(file_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text


def extract_text_from_file(file_path: str, filename: str) -> str:
    """Extract text based on file type"""
    if filename.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif filename.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif filename.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError("Unsupported file type")


def analyze_resume_with_ai(resume_text: str) -> dict:
    """Send resume to Groq AI for analysis"""
    
    prompt = f"""You are an expert resume reviewer and career coach. Analyze this resume and provide detailed feedback.

Resume Content:
{resume_text}

Provide your analysis in the following JSON format (respond ONLY with valid JSON, no other text):
{{
    "overall_score": <number between 1-10>,
    "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
    "weaknesses": ["<weakness 1>", "<weakness 2>", "<weakness 3>"],
    "suggestions": ["<suggestion 1>", "<suggestion 2>", "<suggestion 3>", "<suggestion 4>", "<suggestion 5>"],
    "keywords_missing": ["<keyword 1>", "<keyword 2>", "<keyword 3>"],
    "formatting_feedback": "<brief comment on resume formatting and structure>",
    "summary": "<2-3 sentence overall assessment>"
}}

Be specific, actionable, and honest in your feedback. Respond with ONLY the JSON object, no markdown formatting."""

    try:
        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",  # Fast and powerful model
            temperature=0.7,
            max_tokens=2000,
        )
        
        response_text = chat_completion.choices[0].message.content
        
        # Clean up the response (remove markdown code blocks if present)
        response_text = response_text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Parse JSON from response
        analysis = json.loads(response_text)
        return analysis
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response was: {response_text}")
        # Return a structured fallback
        return {
            "overall_score": 7,
            "strengths": ["Resume received and processed"],
            "weaknesses": ["Unable to perform detailed analysis"],
            "suggestions": ["Please try uploading again"],
            "keywords_missing": [],
            "formatting_feedback": "Standard formatting detected",
            "summary": "Your resume has been received. Please try the analysis again for detailed feedback."
        }
    except Exception as e:
        print(f"Error in AI analysis: {e}")
        return {
            "overall_score": 5,
            "strengths": ["Resume uploaded successfully"],
            "weaknesses": ["Analysis service temporarily unavailable"],
            "suggestions": ["Please try again in a moment"],
            "keywords_missing": [],
            "formatting_feedback": "Unable to analyze at this time",
            "summary": f"Error occurred: {str(e)[:100]}"
        }


def generate_interview_questions(resume_text: str) -> dict:
    """Generate interview questions based on resume"""
    
    prompt = f"""You are an expert interviewer. Based on this resume, generate relevant interview questions.

Resume Content:
{resume_text}

Generate questions in the following JSON format (respond ONLY with valid JSON, no other text):
{{
    "technical_questions": ["<question 1>", "<question 2>", "<question 3>", "<question 4>", "<question 5>"],
    "behavioral_questions": ["<question 1>", "<question 2>", "<question 3>", "<question 4>", "<question 5>"],
    "situational_questions": ["<question 1>", "<question 2>", "<question 3>"]
}}

Make questions specific to their actual experience and skills mentioned in the resume. Respond with ONLY the JSON object."""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.8,
            max_tokens=2000,
        )
        
        response_text = chat_completion.choices[0].message.content.strip()
        
        # Clean markdown
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        questions = json.loads(response_text)
        return questions
        
    except Exception as e:
        print(f"Error generating questions: {e}")
        return {
            "technical_questions": [
                "Tell me about your technical skills and experience",
                "Describe a challenging technical problem you solved",
                "What technologies are you most comfortable with?",
                "How do you stay updated with new technologies?",
                "Explain a project you're proud of"
            ],
            "behavioral_questions": [
                "Describe a time you worked on a team project",
                "Tell me about a challenge you overcame",
                "How do you handle tight deadlines?",
                "Describe a time you had to learn something new quickly",
                "Tell me about a mistake you made and what you learned"
            ],
            "situational_questions": [
                "How would you handle conflicting priorities?",
                "What would you do if you disagreed with your manager?",
                "How would you approach a project with unclear requirements?"
            ]
        }


def evaluate_answer(question: str, answer: str) -> dict:
    """Evaluate an interview answer using AI"""
    
    prompt = f"""You are an expert interviewer evaluating a candidate's answer.

Question: {question}
Candidate's Answer: {answer}

Evaluate the answer and provide feedback in JSON format (respond ONLY with valid JSON):
{{
    "score": <number between 1-10>,
    "feedback": "<detailed feedback on the answer>",
    "suggestions": ["<suggestion 1>", "<suggestion 2>"],
    "strong_points": ["<strong point 1>", "<strong point 2>"]
}}

Respond with ONLY the JSON object."""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1500,
        )
        
        response_text = chat_completion.choices[0].message.content.strip()
        
        # Clean markdown
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        evaluation = json.loads(response_text)
        return evaluation
        
    except Exception as e:
        print(f"Error evaluating answer: {e}")
        return {
            "score": 6,
            "feedback": "Thank you for your answer. Try to provide more specific examples and details.",
            "suggestions": [
                "Include concrete examples from your experience",
                "Structure your answer with a clear beginning, middle, and end"
            ],
            "strong_points": ["You provided a response to the question"]
        }


# ==================== API ENDPOINTS ====================

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"status": "Resume Analyzer API is running!", "version": "3.0 - Groq Powered (Free & Fast)"}


@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and analyze a resume file
    Accepts: PDF, DOCX, TXT
    Returns: Analysis results
    """
    
    # Validate file type
    allowed_extensions = ['.pdf', '.docx', '.txt']
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not supported. Please upload {', '.join(allowed_extensions)}"
        )
    
    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    try:
        # Extract text from file
        resume_text = extract_text_from_file(file_path, file.filename)
        
        if len(resume_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Resume appears to be empty or too short"
            )
        
        # Analyze with AI
        analysis = analyze_resume_with_ai(resume_text)
        
        # Return results
        return {
            "success": True,
            "filename": file.filename,
            "analysis": analysis,
            "resume_text": resume_text[:500] + "..."  # First 500 chars for preview
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)


@app.post("/api/generate-questions")
async def generate_questions(file: UploadFile = File(...)):
    """
    Generate interview questions based on uploaded resume
    """
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    try:
        resume_text = extract_text_from_file(file_path, file.filename)
        questions = generate_interview_questions(resume_text)
        
        return {
            "success": True,
            "questions": questions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


class AnswerEvaluation(BaseModel):
    question: str
    answer: str


@app.post("/api/evaluate-answer")
async def evaluate_answer_endpoint(data: AnswerEvaluation):
    """
    Evaluate a candidate's answer to an interview question
    """
    
    try:
        evaluation = evaluate_answer(data.question, data.answer)
        
        return {
            "success": True,
            "evaluation": evaluation
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating answer: {str(e)}")