FROM python:3.9-slim

RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py /app/
COPY Models /app/Models/

EXPOSE 8082

CMD ["python3", "/app/server.py"]
