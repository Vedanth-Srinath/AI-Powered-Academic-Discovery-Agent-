# rabbit_agent.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file BEFORE importing config
project_root = Path(__file__).parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# Now import config (which will find the API key)
from config.settings import *
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

# The API key check should now work
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# reopen the vector DB built by loader_split_store.py
vectordb = Chroma(
    persist_directory=str(CHROMA_DIR),
    embedding_function=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
)

@tool
def search_papers(question: str) -> str:
    """Search for relevant papers based on the question."""
    docs = vectordb.similarity_search(question, k=SEARCH_K)
    return "\n\n---\n\n".join(d.page_content for d in docs)

# Groq Llama-3
llm = ChatGroq(model=LLM_MODEL, api_key=GROQ_API_KEY)

agent = create_react_agent(
    model=llm,
    tools=[search_papers]
)

