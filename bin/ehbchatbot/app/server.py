import os
from dotenv import load_dotenv


load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv('AZURE_SEARCH_ENDPOINT')
AZURE_SEARCH_KEY = os.getenv('AZURE_SEARCH_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_EMBEDDINGS_DEPLOYMENT = os.getenv('AZURE_EMBEDDINGS_DEPLOYMENT')
AZURE_CHAT_DEPLOYMENT = os.getenv('AZURE_CHAT_DEPLOYMENT')
AZURE_SEARCH_INDEX_NAME = os.getenv('AZURE_SEARCH_INDEX_NAME')
OPENAI_API_VERSION = os.getenv('OPENAI_API_VERSION')

# Ensure all environment variables are set
if not all([AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_EMBEDDINGS_DEPLOYMENT, AZURE_CHAT_DEPLOYMENT, AZURE_SEARCH_INDEX_NAME, OPENAI_API_VERSION]):
    raise ValueError("One or more environment variables are not set")

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from rag_azure_search import chain as rag_azure_search_chain

# Initialize the FastAPI app
app = FastAPI()

# Add the RAG Azure Search route
add_routes(app, rag_azure_search_chain, path="/rag-azure-search")

# Redirect root to docs
@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
8