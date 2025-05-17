import logging

from scraper import get_articles_from_sitemap
from embedder import embed_articles
from pinecone_client import get_index, upsert_articles

logging.basicConfig(level=logging.INFO)


class NewsIngestionPipeline:
    def __init__(self):
        self.index = None
        self.articles = []
        self.embedded_articles = []

    def run(self):
        logging.info("Iniciando pipeline de ingestão de notícias...\n")

        if not self.scrape_articles():
            logging.warning("Nenhum artigo foi extraído do sitemap.")
            return

        if not self.embed_articles():
            logging.warning("Nenhum embedding foi gerado.")
            return

        self.upsert_to_pinecone()
        logging.info("\nPipeline de ingestão finalizado com sucesso.")

    def scrape_articles(self) -> bool:
        self.articles = get_articles_from_sitemap()
        return bool(self.articles)

    def embed_articles(self) -> bool:
        self.embedded_articles = embed_articles(self.articles)
        return bool(self.embedded_articles)

    def upsert_to_pinecone(self):
        self.index = get_index()
        upsert_articles(self.index, self.embedded_articles)


if __name__ == "__main__":
    pipeline = NewsIngestionPipeline()
    pipeline.run()
