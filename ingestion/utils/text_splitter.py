import re

from typing import List, Dict


def split_text(text: str, max_words: int = 200) -> List[str]:
    """Divide um texto em chunks com até 'max_words' palavras, preservando frases."""
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = []

    for sentence in sentences:
        words = sum(len(s.split()) for s in current_chunk + [sentence])
        if words <= max_words:
            current_chunk.append(sentence)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def split_articles_into_chunks(articles: List[Dict], max_words: int = 200) -> List[Dict]:
    """Transforma artigos inteiros em múltiplos chunks prontos para embedding."""
    chunked_articles = []

    for article in articles:
        chunks = split_text(article["content"], max_words)
        for idx, chunk in enumerate(chunks):
            chunked_articles.append({
                "chunk_id": f"{article['url'].split('/')[-1]}_chunk_{idx}",
                "article_url": article["url"],
                "title": article["title"],
                "date": article["date"],
                "image_url": article.get("image_url", ""),
                "content": chunk,
                "position": idx
            })

    return chunked_articles
