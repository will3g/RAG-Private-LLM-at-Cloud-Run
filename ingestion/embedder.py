import logging

from sentence_transformers import SentenceTransformer
from typing import List, Dict

from utils.text_splitter import split_articles_into_chunks

logging.basicConfig(level=logging.INFO)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

logging.info(f"Carregando modelo de embedding: {MODEL_NAME}")
model = SentenceTransformer(MODEL_NAME)


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """Gera embeddings para uma lista de textos."""
    return model.encode(texts, convert_to_numpy=True)


def embed_articles(articles: List[Dict]) -> List[Dict]:
    """
    Divide os artigos em chunks, embeda os textos e retorna
    lista de chunks com embeddings prontos para o Pinecone.
    """
    logging.info(f"Realizando split dos artigos em chunks...")
    chunked_articles = split_articles_into_chunks(articles, max_words=200)

    texts = [chunk["content"] for chunk in chunked_articles]
    logging.info(f"Gerando embeddings para {len(texts)} chunks...")

    embeddings = generate_embeddings(texts)

    embedded_chunks = []
    for chunk, embedding in zip(chunked_articles, embeddings):
        embedded_chunks.append({
            **chunk,
            "embedding": embedding.tolist()
        })

    logging.info(f"Embeddings gerados para todos os chunks.")
    return embedded_chunks


if __name__ == "__main__":
    from scraper import get_articles_from_sitemap

    print("Executando scraping + split + embedding (modo teste)...")
    articles = get_articles_from_sitemap()
    embedded = embed_articles(articles)

    print("\nExemplo de chunk com embedding:")
    print(f"Título: {embedded[0]['title']}")
    print(f"Chunk ID: {embedded[0]['chunk_id']}")
    print(f"Embedding (dimensão): {len(embedded[0]['embedding'])}")
    print(f"Texto:\n{embedded[0]['content'][:300]}...")
