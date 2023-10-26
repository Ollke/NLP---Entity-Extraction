# Use a imagem oficial do Python como base
FROM python:3.8

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo Python (código) para o diretório de trabalho no contêiner
COPY main.py /app

# Instale as dependências do seu aplicativo
RUN pip install fastapi uvicorn spacy pydantic

# Baixe o modelo do spaCy (en_core_web_sm)
RUN python -m spacy download en_core_web_sm

# Baixe o modelo do spaCy (pt_core_news_sm)
RUN python -m spacy download pt_core_news_sm

# Expõe a porta em que o aplicativo estará em execução
EXPOSE 3000

# Comando para executar o aplicativo quando o contêiner for iniciado
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
