FROM python:3.9-slim

RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /app

COPY wait-for-it.sh /app/
RUN chmod +x /app/wait-for-it.sh

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY client.py /app/

CMD ["/app/wait-for-it.sh", "server:8082", "--", "python3", "/app/client.py"]
