import os
import requests
import logging

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
OLLAMA_CLIENT_TOKEN = os.getenv("OLLAMA_CLIENT_TOKEN")

assert OLLAMA_API_URL, "OLLAMA_API_URL não está definido no .env"

def query_ollama(prompt: str) -> str:
    """Envia o prompt para o Ollama Cloud Run e retorna a resposta."""
    try:
        logging.info("Enviando requisição para o modelo no Cloud Run...")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_identity_token()}"
        }

        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(OLLAMA_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(payload)
        return data.get("response", "Nenhuma resposta retornada pelo modelo.")

    except Exception as e:
        logging.error(f"Erro ao consultar o modelo Ollama: {e}")
        return "Erro ao consultar o modelo."


def get_identity_token() -> str:
    """Retorna o token do .env ou gera um novo se não existir."""
    if OLLAMA_CLIENT_TOKEN: return OLLAMA_CLIENT_TOKEN

    try:
        from google.auth.transport.requests import Request
        from google.auth import default

        creds, _ = default()
        creds.refresh(Request())
        return creds.token
    except Exception as e:
        logging.error(f"Erro ao obter token de identidade: {e}")
        return ""
