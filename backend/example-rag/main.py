import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from util import (
    load_and_process_json, convert_to_documents, split_documents, 
    create_vectorstore, retrieve_initial_docs, filter_docs_by_score, 
    extract_relevance_score, generate_response, raise_not_found_exception
)

# Load environment variables and set up logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)

# Initialize FastAPI app
app = FastAPI()

# Define QueryRequest model
class QueryRequest(BaseModel):
    query: str

# Load and process the JSON file
data = load_and_process_json("SyntheticStartupDataset.json")
documents = convert_to_documents(data)
texts = split_documents(documents)

# Create vectorstore
vectorstore = create_vectorstore(texts)

# Initialize the LLM
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

@app.put("/query")
async def query_json(request: QueryRequest):
    try:
        # Step 1: Initial retrieval of documents
        initial_docs = retrieve_initial_docs(vectorstore, request.query)
        
        if not initial_docs:
            raise_not_found_exception("No documents found in initial retrieval.")

        # Step 2: Filter documents by similarity score
        filtered_docs = filter_docs_by_score(initial_docs)
        if not filtered_docs:
            raise_not_found_exception("No documents passed the similarity score threshold.")

        # Step 3: Re-rank documents using LLM and generate responses
        response_list = [
            generate_response(llm, doc, request.query)
            for doc in filtered_docs
            if extract_relevance_score(llm, request.query, doc) >= 7
        ]

        if not response_list:
            raise_not_found_exception("No relevant startups found after LLM re-ranking.")

        return {"results": response_list}

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
