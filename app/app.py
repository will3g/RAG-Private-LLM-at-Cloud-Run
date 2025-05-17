import streamlit as st

from model import answer_question_with_rag


st.set_page_config(page_title="Notícias (RAG)", layout="wide")
st.title("Notícias com IA + RAG")
st.markdown("Este sistema utiliza **IA generativa com RAG** para responder perguntas com base em notícias recentes do O Globo.")

st.divider()

# Input do usuário
question = st.text_input("Faça sua pergunta:", placeholder="Ex: O que está acontecendo com a economia brasileira? / Dormir mais de nove horas por noite está associado à piora no desempenho cognitivo?")

if st.button("Buscar Resposta"):
    if question.strip():
        with st.spinner("Consultando base vetorial e gerando resposta..."):
            response = answer_question_with_rag(question)

        # Resposta
        st.subheader("Resposta da IA:")
        st.markdown(response["answer"])

        # Contexto
        with st.expander("Chunks utilizados (contexto recuperado)"):
            for i, chunk in enumerate(response["retrieved_chunks"], 1):
                metadata = chunk["metadata"]
                st.markdown(f"**Chunk {i}** (score: {chunk['score']:.4f})")
                st.markdown(f"- *{metadata.get('title', 'Sem título')}*")
                st.markdown(f"- [Acessar matéria original]({metadata.get('article_url', '')})")
                st.markdown(f"- Trecho:\n\n> {metadata['content'][:500]}...")

        # Prompt
        with st.expander("Prompt enviado ao modelo"):
            st.code(response["prompt"], language="markdown")

    else:
        st.warning("Por favor, insira uma pergunta para continuar.")
