from langchain_community.document_loaders import ArxivLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from config.settings import *
import os

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

print("📥 Downloading papers...")
# 1. download a few recent papers that match your topic
papers = ArxivLoader(
    query="unsupervised machine learning in life sciences",
    load_max_docs=MAX_DOCS
).load()

print(f"📄 Found {len(papers)} papers. Splitting into chunks...")
# 2. slice each PDF into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE, 
    chunk_overlap=CHUNK_OVERLAP
)
chunks = splitter.split_documents(papers)

print("🔗 Creating embeddings and storing in vector database...")
# 3. embed locally and save into a Chroma folder
emb = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    encode_kwargs={"device": "cpu"}
)

vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=emb,
    persist_directory=str(CHROMA_DIR)
)

print(f"📚 Vector store ready with {len(chunks)} chunks")
print(f"💾 Database saved to: {CHROMA_DIR}")