# Usar uma imagem base Python
FROM python:3.9-slim

# Definir diretório de trabalho no contêiner
WORKDIR /app

# Copiar os arquivos do servidor para o diretório de trabalho
COPY . /app

RUN pip install -r requirements.txt

# Expor a porta 8082 (a porta onde o servidor estará rodando)
EXPOSE 8082

# Definir o comando padrão para rodar o servidor
CMD ["python3", "server.py"]''
