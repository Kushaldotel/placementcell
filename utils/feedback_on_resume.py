import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage
import re
import json

# Load the API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY)

def generate_feedback(resume_text, job_description):
    """
    Generate feedback for a resume based on a job description.
    Returns structured data with feedback, current score, and expected score.
    """
    system_prompt = SystemMessage(content="""
    You are an ATS system that evaluates resumes based on job descriptions.

    First, analyze the resume against the job description and determine:
    1. A current ATS score (out of 100)
    2. An expected ATS score (out of 100) if the candidate implements your suggestions

    Then, provide your evaluation in the following format:
    1. Start with "## ATS Resume Evaluation"
    2. Include the job title from the job description
    3. Provide an ATS Score out of 100 (e.g., "ATS Score: 85/100")
    4. List strengths and weaknesses in bullet points
    5. Provide suggested improvements in numbered list format
    6. End with a conclusion that includes the expected score after improvements

    Be specific, detailed, and actionable in your feedback.

    After your analysis, return a JSON object with the following structure:
    {
        "feedback": "Your detailed feedback in markdown format",
        "current_score": 85,
        "expected_score": 95
    }

    The JSON should be valid and parseable.
    """)

    user_prompt = HumanMessage(content=f"Here is a resume:\n{resume_text}\n\nHere is the job description:\n{job_description}\n\nEvaluate the resume, provide an ATS score (out of 100), and suggest improvements. Return your response in the JSON format specified.")

    # Get response from Gemini
    response = llm.invoke([system_prompt, user_prompt])

    try:
        # Try to parse the response as JSON
        result = json.loads(response.content)
        return result
    except json.JSONDecodeError:
        # If JSON parsing fails, extract scores using regex and create structured response
        feedback_content = response.content

        # Extract current score
        current_score_match = re.search(r'ATS Score:\s*(\d+)\/100', feedback_content)
        current_score = int(current_score_match.group(1)) if current_score_match else 70

        # Extract expected score or estimate it
        expected_score_match = re.search(r'expected score (?:of|after).*?(\d+)', feedback_content, re.IGNORECASE)
        if expected_score_match:
            expected_score = int(expected_score_match.group(1))
        else:
            # Fallback: estimate expected score as current + 15% improvement
            expected_score = min(99, int(current_score * 1.15))

        return {
            "feedback": feedback_content,
            "current_score": current_score,
            "expected_score": expected_score
        }
