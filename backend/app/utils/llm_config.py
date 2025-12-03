from crewai import LLM
import os

def llm_config():
    return LLM(
    model="gemini/gemini-2.5-flash",
    api_version=os.getenv('MODEL'),
    api_key=os.getenv('GEMINI_API_KEY')
)