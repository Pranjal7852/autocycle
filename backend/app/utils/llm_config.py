from crewai import LLM
import os

def llm_config():
    # Use Gemini model via LiteLLM which CrewAI supports natively
    # The 'gemini/' prefix tells LiteLLM to route it to Google AI
    model_name = os.getenv("MODEL", "gemini/gemini-1.5-pro")
    api_key = os.getenv("GEMINI_API_KEY")
    
    return LLM(
        model=model_name,
        api_key=api_key
    )