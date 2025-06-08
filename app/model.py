import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm.rag_query import retrieve_chunks, build_prompt
from llm.ollama_client import query_ollama

def answer_question_with_rag(question: str, top_k: int = 5) -> dict:
    """
    Realiza todo o fluxo RAG:
    - Gera embedding da pergunta
    - Busca os chunks mais relevantes no Pinecone
    - Monta um prompt com contexto
    - Envia para o modelo (Ollama)
    
    Retorna:
        dict com:
            - question: str
            - prompt: str
            - answer: str
            - retrieved_chunks: List[dict]
    """
    # Etapa 1: Recuperar os chunks mais relevantes
    retrieved_chunks = retrieve_chunks(query=question, top_k=top_k)

    # Etapa 2: Montar o prompt com base nos chunks
    prompt = build_prompt(query=question, retrieved_chunks=retrieved_chunks)

    # Etapa 3: Enviar para o modelo via Ollama
    answer = query_ollama(prompt=prompt)

    return {
        "question": question,
        "prompt": prompt,
        "answer": answer,
        "retrieved_chunks": retrieved_chunks
    }
