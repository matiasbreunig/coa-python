# Use a imagem base do Python
FROM python:3.9

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código do aplicativo para o diretório de trabalho
COPY main.py .
COPY dictionary .
COPY dictionary.huawei .
COPY dictionary.freeradius .

# Defina as variáveis de ambiente
ENV NAS_SERVER="186.194.172.2"
ENV NAS_SECRET="senha@uneinternet"
ENV NAS_PORT="3799"
ENV TOKEN="b8e8251c-319d-4f87-b9f0-d53e2f2d5093" 

# Exponha a porta do servidor
EXPOSE 8000

# Execute o aplicativo FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]