FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    python3-dev \
    build-essential \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/* \

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
