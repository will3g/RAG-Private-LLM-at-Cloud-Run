FROM ollama/ollama:0.6.6

ENV OLLAMA_HOST 0.0.0.0:8888
EXPOSE 8888

ENV OLLAMA_MODELS /models

ENV OLLAMA_DEBUG false

# Never unload model weights from the GPU
ENV OLLAMA_KEEP_ALIVE -1

ENV MODEL llama3.2:1b
RUN ollama serve & sleep 5 && ollama pull $MODEL 

ENTRYPOINT ["ollama", "serve"]
