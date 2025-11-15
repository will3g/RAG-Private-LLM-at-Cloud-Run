import requests
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from typing import List, Dict

SITEMAP_URL = "https://oglobo.globo.com/sitemap/oglobo/news.xml"


def fetch_sitemap_xml(url: str) -> str:
    """Faz o download do XML do sitemap."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_sitemap(xml_content: str) -> List[Dict]:
    """Extrai URLs, datas e títulos do sitemap XML."""
    ns = {
        "news": "http://www.google.com/schemas/sitemap-news/0.9",
        "image": "http://www.google.com/schemas/sitemap-image/1.1",
        "": "http://www.sitemaps.org/schemas/sitemap/0.9",
    }

    root = ET.fromstring(xml_content)
    articles = []

    for url in root.findall("url", ns):
        loc = url.find("loc", ns).text
        title = url.find("news:news/news:title", ns).text
        publication_date = url.find("news:news/news:publication_date", ns).text
        image_url = url.find("image:image/image:loc", ns)
        image_url = image_url.text if image_url is not None else None

        articles.append({
            "url": loc,
            "title": title,
            "date": publication_date,
            "image_url": image_url,
        })

    return articles


def scrape_article_text(url: str) -> str:
    """Extrai o corpo principal da matéria do O Globo."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        article = soup.find("article")
        if article:
            return article.get_text(separator="\n", strip=True)

        # fallback (usado em algumas páginas)
        content_div = soup.find("div", {"class": "content-text"})
        if content_div:
            return content_div.get_text(separator="\n", strip=True)

        return None

    except Exception as e:
        print(f"[ERRO] ao fazer scraping de {url}: {e}")
        return None


def get_articles_from_sitemap() -> List[Dict]:
    """Executa o pipeline completo de scraping a partir do sitemap."""
    print("Baixando sitemap...")
    xml_content = fetch_sitemap_xml(SITEMAP_URL)
    raw_articles = parse_sitemap(xml_content)

    print(f"{len(raw_articles)} matérias encontradas no sitemap.")

    articles_with_content = []

    for article in raw_articles:
        print(f"Extraindo conteúdo: {article['url']}")
        content = scrape_article_text(article["url"])
        if content:
            articles_with_content.append({
                **article,
                "content": content
            })
        if len(articles_with_content) == 10: break # REMOVER CASO QUEIRA INSERIR MAIS DADOS: FIM DE DEMONSTRAÇÃO

    print(f"{len(articles_with_content)} matérias com conteúdo extraído.")
    return articles_with_content


if __name__ == "__main__":
    artigos = get_articles_from_sitemap()
    for art in artigos[:3]:
        print(f"\nURL: {art['url']}")
        print(f"Título: {art['title']}")
        print(f"Data: {art['date']}")
        print(f"Trecho: {art['content'][:300]}...\n")
