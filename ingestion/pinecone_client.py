import os
import logging

from typing import List, Dict
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()
logging.basicConfig(level=logging.INFO)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", 'aws')
PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT")
INDEX_NAME = os.getenv("INDEX_NAME", "oglobo-news")
NAMESPACE = os.getenv("PINECONE_NAMESPACE", "default")

assert PINECONE_API_KEY, "PINECONE_API_KEY não definido"
assert PINECONE_ENV, "PINECONE_ENVIRONMENT não definido"

pinecone = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)

def get_index():
    """Retorna o índice Pinecone, cria se não existir"""
    existing_indexes = [index["name"] for index in pinecone.list_indexes()]
    if INDEX_NAME not in existing_indexes:
        logging.info(f"Criando índice: {INDEX_NAME}")
        pinecone.create_index(
            name=INDEX_NAME,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=PINECONE_CLOUD,
                region=PINECONE_ENV
            )
        )
    return pinecone.Index(INDEX_NAME)

def vector_creator(chunks: List[Dict]) -> List[Dict]:
    """
    Converte uma lista de chunks em vetores com metadados estruturados
    """
    _vectors = []
    for chunk in chunks:
        _vectors.append({
            "id": chunk["chunk_id"],
            "values": chunk["embedding"],
            "metadata": {
                "article_url": chunk["article_url"],
                "title": chunk["title"],
                "content": chunk["content"],
                "date": chunk["date"],
                "position": chunk.get("position", 0),
                "image_url": chunk['image_url'] if chunk['image_url'] else ''
            }
        })
    return _vectors

def upsert_articles(index, chunks: List[Dict], namespace: str = NAMESPACE):
    """
    Realiza o upsert dos chunks (com embeddings) no índice Pinecone
    """
    logging.info(f"Inserindo {len(chunks)} chunks no índice '{INDEX_NAME}'...")

    vectors = vector_creator(chunks)

    try:
        index.upsert(vectors=vectors, namespace=namespace)
        logging.info("Todos os chunks foram inseridos com sucesso.")
    except Exception as err:
        logging.error(f'[UPSERT ARTICLES] Error: {err}')


if __name__ == "__main__":
    from scraper import get_articles_from_sitemap
    from embedder import embed_articles

    logging.info("Iniciando teste de ingestão...")
    articles = get_articles_from_sitemap()
    embedded_chunks = embed_articles(articles)

    idx = get_index()
    upsert_articles(idx, embedded_chunks)
