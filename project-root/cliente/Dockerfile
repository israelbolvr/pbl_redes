# Usar uma imagem base Python
FROM python:3.9-slim

# Definir diretório de trabalho no contêiner
WORKDIR /app

# Copiar os arquivos do cliente para o diretório de trabalho
COPY . /app

RUN pip install -r requirements.txt

# Definir o comando padrão para rodar o cliente
CMD ["python3", "client.py"]
