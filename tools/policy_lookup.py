import os
import re
import requests
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.tools import tool

load_dotenv()

VECTOR_DB_NAME=os.getenv('VECTOR_DB_NAME')
VECTOR_DB_PATH=os.getenv('VECTOR_DB_PATH')

def generate_embeddings(path: str):
    response = requests.get(
        "https://storage.googleapis.com/benchmarks-artifacts/travel-db/swiss_faq.md"
    )
    response.raise_for_status()
    faq_text = response.text

    docs = [txt for txt in re.split(r"(?=\n##)", faq_text)]
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    vector_store = Chroma(
        collection_name=VECTOR_DB_NAME,
        create_collection_if_not_exists=True,
        persist_directory=path,
        embedding_function=embeddings
    )

    vector_store.add_texts(texts=docs)


# generate_embeddings(VECTOR_DB_PATH)

VECTOR_STORE = Chroma(
        collection_name=VECTOR_DB_NAME,
        persist_directory=VECTOR_DB_PATH,
        embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    )

@tool
def lookup_policy(query: str) -> str:
    """Consult the company policies to check whether certain options are permitted.
    Use this before making any flight changes performing other 'write' events."""
    
    docs = VECTOR_STORE.similarity_search(query, k=2)
    return "\n\n".join([doc.page_content for doc in docs])