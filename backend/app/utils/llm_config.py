from crewai import LLM
import os

def llm_config():
    return LLM(
     model="azure/gpt-4.1",
    api_version=os.getenv('AZURE_API_VERSION')
)