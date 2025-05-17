import os
import logging

from typing import List
from dotenv import load_dotenv

from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

from llm.ollama_client import query_ollama

load_dotenv()
logging.basicConfig(level=logging.INFO)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
embedder = SentenceTransformer(MODEL_NAME)

# Init pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT")
INDEX_NAME = os.getenv("INDEX_NAME", "oglobo-news")
NAMESPACE = os.getenv("PINECONE_NAMESPACE", "default")

assert PINECONE_API_KEY, "PINECONE_API_KEY não definido"
assert PINECONE_ENV, "PINECONE_ENVIRONMENT não definido"

pinecone = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
index = pinecone.Index(INDEX_NAME)


def generate_query_embedding(query: str) -> List[float]:
    return embedder.encode(query, convert_to_numpy=True).tolist()


def retrieve_chunks(query: str, top_k: int = 5) -> List[dict]:
    embedding = generate_query_embedding(query)
    logging.info("Buscando chunks relevantes no Pinecone...")

    res = index.query(vector=embedding, top_k=top_k, namespace=NAMESPACE, include_metadata=True)
    return res["matches"]


def build_prompt(query: str, retrieved_chunks: List[dict]) -> str:
    context_blocks = []
    for match in retrieved_chunks:
        content = match["metadata"]["content"]
        title = match["metadata"].get("title", "")
        context_blocks.append(f"Título: {title}\nTrecho: {content}")

    context_text = "\n\n".join(context_blocks)
    prompt = (
        f"Contexto relevante extraído de notícias recentes:\n\n"
        f"{context_text}\n\n"
        f"Com base nesse contexto, responda de forma clara e direta:\n"
        f"{query}"
    )
    return prompt


def answer_with_rag(query: str, top_k: int = 5) -> str:
    retrieved = retrieve_chunks(query, top_k=top_k)
    if not retrieved:
        return "Nenhuma informação relevante encontrada."

    prompt = build_prompt(query, retrieved)
    logging.info("Enviando prompt ao modelo via Ollama...")
    response = query_ollama(prompt)
    return response


# Teste local
if __name__ == "__main__":
    pergunta = "Quais foram os principais pontos do estudo de variações de genes no DNA dos brasileiros?"
    resposta = answer_with_rag(pergunta)
    print("\n Resposta gerada:")
    print(resposta)
