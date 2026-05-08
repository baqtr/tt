FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV WALLET="86HoPo7YGXU66KN4L7EsMzDcNTWDpbNmd455TW18ozuoSe1JeW2pzUSUabLPEcCwG58E3jPHYLnQYB3F5ouZ7n1J4TaknW4"
ENV PYTHONUNBUFFERED=1

CMD ["python", "miner.py"]