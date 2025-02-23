import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage

# Load the API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GEMINI_API_KEY)

def generate_feedback(resume_text, job_description):
    """
    Generate feedback for a resume based on a job description.
    """
    system_prompt = SystemMessage(content="You are an ATS system that evaluates resumes based on job descriptions.")
    user_prompt = HumanMessage(content=f"Here is a resume:\n{resume_text}\n\nHere is the job description:\n{job_description}\n\nEvaluate the resume, provide an ATS score (out of 100), and suggest improvements.")

    # Get response from Gemini
    response = llm.invoke([system_prompt, user_prompt])
    return response.content
