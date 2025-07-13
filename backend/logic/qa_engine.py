import os
import openai
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv() 
openai.api_key = os.getenv("OPENAI_API_KEY")

_embeddings = OpenAIEmbeddings()
_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", ".", " "]
)

def prepare_vector_index(document_text: str) -> Optional[FAISS]:
    """
    splits document into chunks, embeds them, and stores in a vector index.
    """
    if not document_text:
        return None
    chunks = _text_splitter.split_text(document_text)
    if not chunks:
        return None
    return FAISS.from_texts(chunks, embedding=_embeddings)

def answer_question(query: str, vector_index: FAISS) -> Optional[str]:
    """
    Uses vector index to find relevant context and generate an answer.
    """
    if not query or not vector_index:
        return None

    docs = vector_index.similarity_search(query, k=3)
    context = "\n---\n".join([doc.page_content for doc in docs])

    prompt = f"""
you are reading a document and answering a question about it.
only use the context below, do not guess beyond it.

Context:
{context}

Question:
{query}

Answer in 2-4 sentences and include a justification based on the context.
    """.strip()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=300
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception:
        return None


