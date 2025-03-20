import json
import logging
from fastapi import HTTPException
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document, AIMessage

# Constants
JSON_FILE_PATH = "RealStartupDataset.json"
K_VALUE = 10
SIMILARITY_THRESHOLD = 0.35
RELEVANCE_THRESHOLD = 7

# Utility Functions
def load_and_process_json(file_path: str) -> list:
    """Load and process the JSON data from the given file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Data file not found.")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Invalid JSON data.")

def convert_to_documents(data: list) -> list:
    """Convert a list of dictionaries into a list of Document objects."""
    return [
        Document(
            page_content=item['Description'],
            metadata={"Startup Name": item['Startup Name'], "Website": item['Website']}
        )
        for item in data
    ]

def split_documents(documents: list) -> list:
    """Split documents into smaller chunks using a text splitter."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(documents)

def create_vectorstore(texts: list) -> FAISS:
    """Create a FAISS vector store from the given texts and embeddings."""
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(texts, embeddings)

def retrieve_initial_docs(vectorstore: FAISS, query: str, k: int = K_VALUE) -> list:
    """Retrieve initial documents based on similarity score."""
    return vectorstore.similarity_search_with_score(query, k)

def filter_docs_by_score(initial_docs: list, threshold: float = SIMILARITY_THRESHOLD) -> list:
    """Filter documents by similarity score threshold."""
    return [doc for doc, score in initial_docs if score > threshold]

def extract_relevance_score(llm: ChatOpenAI, query: str, doc: Document) -> int:
    """Extract relevance score from LLM."""
    ranking_prompt = create_ranking_prompt(query, doc)
    ranking_result = llm.invoke(ranking_prompt)
    try:
        return int(ranking_result.content.strip())
    except ValueError:
        logging.info(f"Failed to parse relevance score for document: {doc.metadata['Startup Name']}")
        return 0

def generate_response(llm: ChatOpenAI, doc: Document, query: str) -> dict:
    """Generate a structured response using LLM."""
    retrieval_prompt = create_retrieval_prompt(doc)
    result = llm.invoke(retrieval_prompt)
    if isinstance(result, AIMessage):
        response_data = parse_json_content(result.content)
        if response_data:
            return {
                "Startup Name": response_data.get("Startup Name", doc.metadata.get('Startup Name', 'N/A')),
                "Website": response_data.get("Website", doc.metadata.get('Website', 'N/A')),
                "Introduction": response_data.get("Introduction", "N/A"),
                "Problem": response_data.get("Problem", "N/A"),
                "Solution": response_data.get("Solution", "N/A")
            }
    return {}

def parse_json_content(content: str) -> dict:
    """Attempt to parse JSON content and return a dictionary."""
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error: {e}")
        return None

def create_ranking_prompt(query: str, doc: Document) -> str:
    """Create a prompt to rank the relevance of a document."""
    return f"""
    A user is asking about startups that work in "{query}". 
    Based on the following information, rate the relevance of this startup on a scale of 1 to 10, 
    where 10 is highly relevant and 1 is not relevant at all.
    Information: {doc.page_content}
    Your response should only contain the relevance score.
    """

def create_retrieval_prompt(doc: Document) -> str:
    """Create a prompt to retrieve detailed information about a startup."""
    return f"""
    You are an AI that helps users learn about startups. 
    Based on the following information, provide a JSON response with the following fields:
    - Startup Name: {doc.metadata.get('Startup Name', 'N/A')}
    - Website: {doc.metadata.get('Website', 'N/A')}
    - Introduction: A short description of what the startup does.
    - Problem: The problem the startup aims to solve.
    - Solution: The solution provided by the startup to solve the mentioned problem.
    Information: {doc.page_content}
    """

def raise_not_found_exception(detail: str):
    """Helper function to raise an HTTP 404 exception with logging."""
    logging.info(detail)
    raise HTTPException(status_code=404, detail=detail)
